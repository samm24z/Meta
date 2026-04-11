from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import InboxAction, InboxObservation
from sample_data import SCENARIOS
from graders import get_partial_reward, grade_action


class TestEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_scenario = None
        self._done = False
        self._last_action = None
        self._score_breakdown = {}

        # 🔥 CRITICAL FIX: local counter (NOT global)
        self._task_index = 0

    def reset(self) -> InboxObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._done = False
        self._last_action = None
        self._score_breakdown = {}

        # ✅ GUARANTEED UNIQUE TASK ROTATION
        self._current_scenario = SCENARIOS[self._task_index % len(SCENARIOS)]
        self._task_index += 1

        valid_slot_ids = [
            slot.slot_id
            for slot in self._current_scenario.available_slots
            if slot.is_available
        ]

        return InboxObservation(
            scenario=self._current_scenario,
            step=0,
            step_feedback="New inbox task loaded. Submit one complete structured action.",
            triage_score=0.0,
            operation_score=0.0,
            draft_score=0.0,
            valid_slot_ids=valid_slot_ids,
            task_id=self._current_scenario.scenario_id,
            reward=0.0,
            done=False,
        )

    def step(self, action: InboxAction) -> InboxObservation:  # type: ignore[override]
        if self._current_scenario is None:
            return InboxObservation(
                scenario=None,
                step=self._state.step_count,
                step_feedback="Environment not initialized. Please call reset() first.",
                triage_score=0.0,
                operation_score=0.0,
                draft_score=0.0,
                valid_slot_ids=[],
                task_id=None,
                reward=0.0,
                done=True,
            )

        if self._done:
            return InboxObservation(
                scenario=self._current_scenario,
                step=self._state.step_count,
                step_feedback="Episode already completed. Please reset.",
                triage_score=self._score_breakdown.get("triage_total", 0.5),
                operation_score=self._score_breakdown.get("scheduling_total", 0.5),
                draft_score=self._score_breakdown.get("response_total", 0.5),
                valid_slot_ids=[
                    slot.slot_id
                    for slot in self._current_scenario.available_slots
                    if slot.is_available
                ],
                task_id=self._current_scenario.scenario_id,
                reward=0.5,
                done=True,
            )

        self._state.step_count += 1
        task_id = self._current_scenario.scenario_id

        penalty = 0.0
        if self._last_action == action.model_dump():
            penalty = -0.05

        self._last_action = action.model_dump()

        reward = get_partial_reward(self._state.step_count, task_id, action) + penalty

        final_score, breakdown = grade_action(task_id, action)
        self._score_breakdown = breakdown

        self._done = True

        return InboxObservation(
            scenario=self._current_scenario,
            step=self._state.step_count,
            step_feedback=f"Action evaluated. Reward: {round(reward, 4)}",
            triage_score=breakdown.get("triage_total", 0.5),
            operation_score=breakdown.get("scheduling_total", 0.5),
            draft_score=breakdown.get("response_total", 0.5),
            valid_slot_ids=[
                slot.slot_id
                for slot in self._current_scenario.available_slots
                if slot.is_available
            ],
            task_id=task_id,
            reward=reward,
            done=True,
        )

    @property
    def state(self) -> State:
        return self._state