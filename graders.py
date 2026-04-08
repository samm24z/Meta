try:
    from models import InboxAction
    from sample_data import GROUND_TRUTH
except ImportError:
    from .models import InboxAction
    from .sample_data import GROUND_TRUTH


def grade_action(task_id: str, action: InboxAction):
    gt = GROUND_TRUTH[task_id]

    score = 0.0
    breakdown = {}

    if action.triage_label == gt["triage_label"]:
        score += 0.15
        breakdown["triage_label"] = 0.15
    else:
        breakdown["triage_label"] = 0.0

    if action.urgency == gt["urgency"]:
        score += 0.1
        breakdown["urgency"] = 0.1
    else:
        breakdown["urgency"] = 0.0

    if action.intent == gt["intent"]:
        score += 0.1
        breakdown["intent"] = 0.1
    else:
        breakdown["intent"] = 0.0

    if action.chosen_operation == gt["chosen_operation"]:
        score += 0.25
        breakdown["operation"] = 0.25
    else:
        breakdown["operation"] = 0.0

    if action.response_draft:
        score += 0.15
        breakdown["response"] = 0.15
    else:
        breakdown["response"] = 0.0

    return score, breakdown


def get_partial_reward(step: int, task_id: str, action: InboxAction):
    score, _ = grade_action(task_id, action)
    return score / 3  # spread across steps