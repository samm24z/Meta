from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import InboxAction, InboxObservation
from sample_data import SCENARIOS
from .graders import grade_action


class TestEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_index = 0
        self._done = False

    def reset(self) -> InboxObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_index = 0
        self._done = False

        scenario = SCENARIOS[self._current_index]

        return InboxObservation(
            scenario=scenario,
            step=0,
            step_feedback="Start",
            triage_score=0.0,
            operation_score=0.0,
            draft_score=0.0,
            valid_slot_ids=[s.slot_id for s in scenario.available_slots],
            task_id=scenario.scenario_id,
            reward=0.0,
            done=False,
        )

    def step(self, action: InboxAction) -> InboxObservation:
        scenario = SCENARIOS[self._current_index]
        task_id = scenario.scenario_id

        score, breakdown = grade_action(task_id, action)

        # 🔥 FORCE VALID RANGE
        score = max(0.1, min(score, 0.9))

        self._current_index += 1
        self._state.step_count += 1

        done = self._current_index >= len(SCENARIOS)

        next_scenario = None
        if not done:
            next_scenario = SCENARIOS[self._current_index]

        return InboxObservation(
            scenario=next_scenario,
            step=self._state.step_count,
            step_feedback="Next task",
            triage_score=0.5,
            operation_score=0.5,
            draft_score=0.5,
            valid_slot_ids=[s.slot_id for s in next_scenario.available_slots] if next_scenario else [],
            task_id=task_id,
            reward=score,
            done=done,
        )

    @property
    def state(self) -> State:
        return self._state