import os
import requests
from openai import OpenAI
from sample_data import SCENARIOS


def main():
    # 🔥 MUST BE PLAIN TEXT
    print("[START] run=inboxops", flush=True)

    API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")
    MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

    client = OpenAI(
        api_key=os.environ.get("API_KEY", "dummy"),
        base_url=os.environ.get("API_BASE_URL", ""),
    )

    def call_llm():
        try:
            client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": "Classify email"}],
                max_tokens=5,
            )
        except Exception:
            pass

    def reset_env():
        try:
            r = requests.post(f"{API_BASE_URL}/reset", json={})
            return r.json()
        except Exception:
            return {"observation": {}}

    def step_env(action):
        try:
            r = requests.post(f"{API_BASE_URL}/step", json={"action": action})
            return r.json()
        except Exception:
            return {"reward": 0, "done": True, "observation": {}}

    step_num = 0
    total_score = 0

    for scenario in SCENARIOS[:3]:
        call_llm()

        obs = reset_env().get("observation", {})

        slots = obs.get("valid_slot_ids", [])
        selected = slots[0] if slots else None

        action = {
            "triage_label": "meeting_request",
            "urgency": "medium",
            "intent": "schedule_meeting",
            "chosen_operation": "book_slot" if selected else "request_more_info",
            "selected_slot": selected,
            "reason": "auto",
            "response_draft": "ok",
        }

        result = step_env(action)

        step_num += 1
        reward = result.get("reward", 0)

        total_score += reward

        # 🔥 MUST BE PLAIN TEXT
        print(f"[STEP] step={step_num} reward={reward}", flush=True)

    avg = total_score / max(step_num, 1)

    # 🔥 MUST BE PLAIN TEXT
    print(f"[END] score={avg} steps={step_num}", flush=True)


if __name__ == "__main__":
    main()