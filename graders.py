try:
    from models import InboxAction
    from sample_data import GROUND_TRUTH
except ImportError:
    from .models import InboxAction
    from .sample_data import GROUND_TRUTH


def grade_action(task_id: str, action: InboxAction):
    gt = GROUND_TRUTH[task_id]

    triage_score = 0.0
    operation_score = 0.0
    response_score = 0.0

    # TRIAGE
    if action.triage_label == gt["triage_label"]:
        triage_score += 0.2
    if action.urgency == gt["urgency"]:
        triage_score += 0.1
    if action.intent == gt["intent"]:
        triage_score += 0.1

    # OPERATION
    if action.chosen_operation == gt["chosen_operation"]:
        operation_score += 0.3

    # RESPONSE
    if action.response_draft:
        response_score += 0.2

    total_score = triage_score + operation_score + response_score

    # 🔥 IMPORTANT: MATCH ENV KEYS EXACTLY
    breakdown = {
        "triage_total": triage_score,
        "scheduling_total": operation_score,
        "response_total": response_score,
    }

    return total_score, breakdown


def get_partial_reward(step: int, task_id: str, action: InboxAction):
    score, _ = grade_action(task_id, action)

    # 🔥 ALWAYS SAFE RANGE
    safe_score = max(0.1, min(score, 0.9))

    return safe_score