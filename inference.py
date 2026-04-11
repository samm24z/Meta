import os
import requests
from sample_data import SCENARIOS

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")


def safe_post(url, payload=None):
    try:
        res = requests.post(url, json=payload or {})
        res.raise_for_status()
        return res.json()
    except Exception:
        return None


def reset_env():
    return safe_post(f"{API_BASE_URL}/reset")


def step_env(action):
    return safe_post(f"{API_BASE_URL}/step", {"action": action})


def build_action(obs):
    scenario = obs.get("scenario", {})
    slots = obs.get("valid_slot_ids", [])

    slot = slots[0] if slots else None

    return {
        "triage_label": "meeting_request",
        "urgency": "medium",
        "intent": "schedule_meeting",
        "chosen_operation": "book_slot" if slot else "request_more_info",
        "selected_slot": slot,
        "reason": "Selected earliest valid slot." if slot else "No slots available",
        "response_draft": (
            f"Hi {scenario.get('sender_name', 'there')}, "
            f"I've booked slot {slot}."
            if slot else
            f"Hi {scenario.get('sender_name', 'there')}, please share availability."
        ),
    }


def main():
    print(f"[START] run_id=inboxops-baseline api={API_BASE_URL} model={MODEL_NAME}", flush=True)

    results = []
    step_num = 0

    for scenario in SCENARIOS[:3]:
        reset = reset_env()
        if not reset:
            continue

        obs = reset.get("observation", {})
        task_id = scenario.scenario_id

        action = build_action(obs)
        step = step_env(action)

        if not step:
            continue

        step_num += 1

        reward = step.get("reward", 0)
        done = step.get("done", True)

        print(f"[STEP] step={step_num} task_id={task_id} reward={reward} done={done}", flush=True)

        ob = step.get("observation", {})
        results.append(
            ob.get("triage_score", 0)
            + ob.get("operation_score", 0)
            + ob.get("draft_score", 0)
        )

    avg = sum(results) / len(results) if results else 0

    print(f"[END] average_score={avg} task_count={len(results)}", flush=True)


if __name__ == "__main__":
    main()