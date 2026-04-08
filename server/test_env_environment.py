# server/test_env_environment.py
# InboxOps: Email Triage + Scheduling Assistant Environment

from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import InboxAction, InboxObservation
from sample_data import SCENARIOS
from graders import get_partial_reward, grade_action


class TestEnvironment(Environment):
    """
    InboxOps environment:
    - triages emails
    - handles scheduling decisions
    - drafts responses

    This environment is designed to evaluate a single-step full action:
    the agent receives one inbox scenario and must return a complete,
    structured action containing:
      - triage
      - operation
      - selected slot / reasoning
      - response draft

    Each reset() rotates deterministically through available scenarios.
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    # Global counter so repeated /reset calls rotate across tasks
    GLOBAL_SCENARIO_INDEX = 0

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_scenario = None
        self._done = False
        self._last_action = None
        self._score_breakdown = {}

    def _get_next_scenario(self):
        """Cycle through scenarios globally across resets."""
        scenario = SCENARIOS[TestEnvironment.GLOBAL_SCENARIO_INDEX % len(SCENARIOS)]
        TestEnvironment.GLOBAL_SCENARIO_INDEX += 1
        return scenario

    def reset(self) -> InboxObservation:
        """
        Start a new episode with the next scenario.
        """
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._done = False
        self._last_action = None
        self._score_breakdown = {}

        self._current_scenario = self._get_next_scenario()

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
        """
        Execute one full agent action.

        This environment is evaluated in ONE meaningful decision step:
        - classify the email
        - decide operation
        - choose a slot if needed
        - draft a response

        After one step, the episode is marked done.
        """
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
                step_feedback="Episode already completed. Please reset for a new task.",
                triage_score=self._score_breakdown.get("triage_total", 0.0),
                operation_score=self._score_breakdown.get("scheduling_total", 0.0),
                draft_score=self._score_breakdown.get("response_total", 0.0),
                valid_slot_ids=[
                    slot.slot_id
                    for slot in self._current_scenario.available_slots
                    if slot.is_available
                ],
                task_id=self._current_scenario.scenario_id,
                reward=0.0,
                done=True,
            )

        self._state.step_count += 1
        task_id = self._current_scenario.scenario_id

        # Mild repetition penalty
        penalty = 0.0
        if self._last_action == action.model_dump():
            penalty = -0.05

        self._last_action = action.model_dump()

        # Partial reward (shaping)
        reward = get_partial_reward(task_id, action) + penalty

        # Full grading breakdown
        final_score, breakdown = grade_action(task_id, action)
        self._score_breakdown = breakdown

        self._done = True

        return InboxObservation(
            scenario=self._current_scenario,
            step=self._state.step_count,
            step_feedback=f"Action evaluated. Final reward: {round(reward, 4)}",
            triage_score=breakdown.get("triage_total", 0.0),
            operation_score=breakdown.get("scheduling_total", 0.0),
            draft_score=breakdown.get("response_total", 0.0),
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
        """
        Get current environment state.
        """
        return self._state