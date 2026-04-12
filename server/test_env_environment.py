from sample_data import SCENARIOS


class TestEnvironment:
    def __init__(self):
        self.current_index = 0

    def reset(self):
        scenario = SCENARIOS[self.current_index % len(SCENARIOS)]
        self.current_index += 1

        return {
            "observation": {
                "scenario": {
                    "sender_name": scenario.sender_name,
                    "subject": scenario.subject,
                    "body": scenario.body,
                },
                "valid_slot_ids": [
                    slot.slot_id for slot in scenario.available_slots if slot.is_available
                ],
            },
            "info": {},
        }

    def step(self, action):
        return {
            "observation": {
                "triage_score": 0.5,
                "operation_score": 0.5,
                "draft_score": 0.5,
            },
            "reward": 0.5,
            "done": True,
        }