from typing import Dict, Any
from .sample_data import SCENARIOS
from .models import InboxAction
from .graders import grade_action


class TestEnvironment:
    def __init__(self):
        self.current_index = 0
        self.current_scenario = None

    def reset(self) -> Dict[str, Any]:
        if self.current_index >= len(SCENARIOS):
            self.current_index = 0

        self.current_scenario = SCENARIOS[self.current_index]
        self.current_index += 1

        return {
            "observation": {
                "scenario": {
                    "scenario_id": self.current_scenario.scenario_id,
                    "sender_name": self.current_scenario.sender_name,
                    "subject": self.current_scenario.subject,
                    "body": self.current_scenario.body,
                },
                "valid_slot_ids": [
                    slot.slot_id
                    for slot in self.current_scenario.available_slots
                    if slot.is_available
                ],
            }
        }

    def step(self, action_dict: Dict[str, Any]) -> Dict[str, Any]:
        action = InboxAction(**action_dict)

        task_id = self.current_scenario.scenario_id
        score, breakdown = grade_action(task_id, action)

        return {
            "observation": {
                "triage_score": breakdown.get("triage_label", 0),
                "operation_score": breakdown.get("operation", 0),
                "draft_score": breakdown.get("response", 0),
            },
            "reward": score,
            "done": True,
        }