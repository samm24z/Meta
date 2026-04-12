try:
    from models import InboxAction
    from sample_data import GROUND_TRUTH
except ImportError:
    from .models import InboxAction
    from .sample_data import GROUND_TRUTH


def _score(task_id: str, action: InboxAction):
    gt = GROUND_TRUTH[task_id]

    score = 0.0
    breakdown = {}

    if action.triage_label == gt["triage_label"]:
        score += 0.2
        breakdown["triage_label"] = 0.2
    else:
        breakdown["triage_label"] = 0.05

    if action.urgency == gt["urgency"]:
        score += 0.2
        breakdown["urgency"] = 0.2
    else:
        breakdown["urgency"] = 0.05

    if action.intent == gt["intent"]:
        score += 0.2
        breakdown["intent"] = 0.2
    else:
        breakdown["intent"] = 0.05

    if action.chosen_operation == gt["chosen_operation"]:
        score += 0.3
        breakdown["operation"] = 0.3
    else:
        breakdown["operation"] = 0.1

    if action.response_draft:
        score += 0.1
        breakdown["response"] = 0.1
    else:
        breakdown["response"] = 0.05

    # 🔥 force score strictly between (0,1)
    score = max(0.05, min(score, 0.95))

    return score, breakdown


# ✅ REQUIRED BY SERVER (DO NOT REMOVE)
def grade_action(task_id: str, action: InboxAction):
    return _score(task_id, action)


# ✅ REQUIRED BY VALIDATOR (3 TASKS)
def grade_easy_001(task_id: str, action: InboxAction):
    return _score(task_id, action)


def grade_medium_001(task_id: str, action: InboxAction):
    return _score(task_id, action)


def grade_hard_001(task_id: str, action: InboxAction):
    return _score(task_id, action)