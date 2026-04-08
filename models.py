from typing import Optional, List, Literal, Dict
from pydantic import BaseModel


# ─────────────────────────────────────────────
# CALENDAR + EMAIL STRUCTURES
# ─────────────────────────────────────────────

class CalendarSlot(BaseModel):
    slot_id: str
    day: str
    start_time: str
    end_time: str
    timezone: str = "UTC"
    is_available: bool
    conflict_note: Optional[str] = None


class EmailThread(BaseModel):
    sender: str
    timestamp: str
    body: str


class EmailScenario(BaseModel):
    scenario_id: str
    task_level: Literal["easy", "medium", "hard"]

    subject: str
    body: str

    sender_name: str
    sender_email: str
    sender_role: Optional[str] = None

    thread_history: List[EmailThread] = []
    available_slots: List[CalendarSlot] = []

    policy_notes: Optional[str] = None
    timezone_context: Optional[str] = None


# ─────────────────────────────────────────────
# ACTION MODEL
# ─────────────────────────────────────────────

class InboxAction(BaseModel):

    triage_label: Optional[Literal[
        "meeting_request",
        "reschedule_request",
        "urgent_escalation",
        "follow_up",
        "availability_check",
        "other"
    ]] = None

    urgency: Optional[Literal[
        "low", "medium", "high", "critical"
    ]] = None

    intent: Optional[Literal[
        "schedule_meeting",
        "reschedule_meeting",
        "cancel_meeting",
        "ask_availability",
        "general_query"
    ]] = None

    chosen_operation: Optional[Literal[
        "book_slot",
        "decline",
        "propose_alternative",
        "escalate",
        "request_more_info",
        "no_action_needed"
    ]] = None

    selected_slot: Optional[str] = None
    reason: Optional[str] = None

    response_draft: Optional[str] = None


# ─────────────────────────────────────────────
# OBSERVATION MODEL (IMPORTANT)
# ─────────────────────────────────────────────

class InboxObservation(BaseModel):
    """Clean observation returned to agent."""

    scenario: Optional[EmailScenario] = None

    step: int = 0
    step_feedback: Optional[str] = None

    triage_score: Optional[float] = None
    operation_score: Optional[float] = None
    draft_score: Optional[float] = None

    valid_slot_ids: List[str] = []
    task_id: Optional[str] = None

    reward: float = 0.0
    done: bool = False


# ─────────────────────────────────────────────
# STATE MODEL
# ─────────────────────────────────────────────

class InboxState(BaseModel):
    episode_id: str
    step_count: int = 0
    task_id: Optional[str] = None
    done: bool = False


# ─────────────────────────────────────────────
# GRADER RESPONSE
# ─────────────────────────────────────────────

class GraderResponse(BaseModel):
    task_id: str
    score: float
    breakdown: Dict[str, float]


class BaselineResponse(BaseModel):
    model: str
    scores: Dict[str, float]
    average_score: float