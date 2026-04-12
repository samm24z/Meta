try:
    from models import InboxAction
    from sample_data import GROUND_TRUTH
except ImportError:
    from .models import InboxAction
    from .sample_data import GROUND_TRUTH


def _score(task_id: str, action: InboxAction):
    gt = GROUND_TRUTH[task_id]

    score = 0.0

    if action.triage_label == gt["triage_label"]:
        score += 0.2
    else:
        score += 0.05

    if action.urgency == gt["urgency"]:
        score += 0.2
    else:
        score += 0.05

    if action.intent == gt["intent"]:
        score += 0.2
    else:
        score += 0.05

    if action.chosen_operation == gt["chosen_operation"]:
        score += 0.3
    else:
        score += 0.1

    if action.response_draft:
        score += 0.1
    else:
        score += 0.05

    # ensure strictly between (0,1)
    score = max(0.05, min(score, 0.95))

    return score, {}


# ✅ REQUIRED BY SERVER
def grade_action(task_id: str, action: InboxAction):
    return _score(task_id, action)


# ✅ INDIVIDUAL GRADERS
def grade_easy_001(task_id: str, action: InboxAction):
    return _score(task_id, action)


def grade_medium_001(task_id: str, action: InboxAction):
    return _score(task_id, action)


def grade_hard_001(task_id: str, action: InboxAction):
    return _score(task_id, action)


# 🔥🔥 THIS IS THE REAL FIX 🔥🔥
# Explicit registry so OpenEnv can discover tasks

TASK_GRADERS = {
    "easy_001": grade_easy_001,
    "medium_001": grade_medium_001,
    "hard_001": grade_hard_001,
}