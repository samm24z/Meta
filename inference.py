import os
import requests
import json

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")


def safe_post(url, payload=None):
    try:
        res = requests.post(url, json=payload or {})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(json.dumps({"tag": "[ERROR]", "message": str(e)}))
        return None


def reset_env():
    return safe_post(f"{API_BASE_URL}/reset")


def step_env(action):
    return safe_post(f"{API_BASE_URL}/step", {"action": action})


def build_action(observation):
    scenario = observation.get("scenario", {})
    valid_slots = observation.get("valid_slot_ids", [])

    selected_slot = valid_slots[0] if valid_slots else None
    sender = scenario.get("sender_name", "there")

    return {
        "triage_label": "meeting_request",
        "urgency": "medium",
        "intent": "schedule_meeting",
        "chosen_operation": "book_slot" if selected_slot else "request_more_info",
        "selected_slot": selected_slot,
        "reason": "Selected earliest valid slot." if selected_slot else "No available slots.",
        "response_draft": (
            f"Hi {sender}, thanks for reaching out. "
            f"I've booked the earliest available slot ({selected_slot}). "
            f"Looking forward to speaking."
            if selected_slot else
            f"Hi {sender}, could you share your availability?"
        ),
    }


def main():
    print(json.dumps({
        "tag": "[START]",
        "run_id": "inboxops-baseline-run",
        "api_base_url": API_BASE_URL,
        "model_name": MODEL_NAME,
    }))

    results = []

    for step_num in range(1, 4):  # exactly 3 tasks

        reset_result = reset_env()
        if not reset_result:
            break

        obs = reset_result.get("observation", {})
        task_id = obs.get("task_id", f"task_{step_num}")

        action = build_action(obs)

        step_result = step_env(action)
        if not step_result:
            break

        print(json.dumps({
            "tag": "[STEP]",
            "step": step_num,
            "task_id": task_id,
            "action": action,
            "reward": step_result.get("reward"),
            "done": step_result.get("done"),
        }))

        observation = step_result.get("observation", {})

        results.append({
            "task_id": task_id,
            "triage_score": observation.get("triage_score", 0),
            "operation_score": observation.get("operation_score", 0),
            "draft_score": observation.get("draft_score", 0),
        })

    avg_score = (
        sum(r["triage_score"] + r["operation_score"] + r["draft_score"] for r in results)
        / len(results)
        if results else 0
    )

    print(json.dumps({
        "tag": "[END]",
        "final_score": {
            "per_task": results,
            "average_score": avg_score,
            "task_count": len(results),
        }
    }))


if __name__ == "__main__":
    main()