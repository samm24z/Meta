from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from models import InboxAction, InboxObservation
    from sample_data import SCENARIOS
    from graders import grade_action, get_partial_reward
except ImportError:
    from ..models import InboxAction, InboxObservation
    from ..sample_data import SCENARIOS
    from ..graders import grade_action, get_partial_reward


class TestEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._scenario_index = 0
        self._current_scenario = None
        self._done = False

    def _ensure_scenario(self):
        """
        Makes step() safe even if the server creates a fresh environment instance.
        """
        if self._current_scenario is None:
            self._current_scenario = SCENARIOS[0]

    def reset(self) -> InboxObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._done = False

        self._current_scenario = SCENARIOS[self._scenario_index % len(SCENARIOS)]
        self._scenario_index += 1

        return InboxObservation(
            scenario=self._current_scenario,
            step=0,
            step_feedback="New task loaded",
            valid_slot_ids=[
                s.slot_id for s in self._current_scenario.available_slots if s.is_available
            ],
            task_id=self._current_scenario.scenario_id,
            triage_score=0.0,
            operation_score=0.0,
            draft_score=0.0,
            reward=0.0,
            done=False,
        )

    def step(self, action: InboxAction) -> InboxObservation:
        # 🔥 Fix for stateless server behavior
        self._ensure_scenario()

        self._state.step_count += 1
        task_id = self._current_scenario.scenario_id

        reward = get_partial_reward(self._state.step_count, task_id, action)
        final_score, breakdown = grade_action(task_id, action)

        if action.response_draft is not None or self._state.step_count >= 3:
            self._done = True

        return InboxObservation(
            scenario=self._current_scenario,
            step=self._state.step_count,
            step_feedback="Step evaluated",
            triage_score=breakdown.get("triage_label", 0.0)
            + breakdown.get("urgency", 0.0)
            + breakdown.get("intent", 0.0),
            operation_score=breakdown.get("operation", 0.0),
            draft_score=breakdown.get("response", 0.0),
            valid_slot_ids=[
                s.slot_id for s in self._current_scenario.available_slots if s.is_available
            ],
            task_id=task_id,
            reward=reward,
            done=self._done,
        )

    @property
    def state(self) -> State:
        return self._state