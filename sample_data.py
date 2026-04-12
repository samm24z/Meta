try:
    from server.models import EmailScenario, EmailThread, CalendarSlot
except ImportError:
    from .models import EmailScenario, EmailThread, CalendarSlot


SCENARIOS = [
    EmailScenario(
        scenario_id="easy_001",
        task_level="easy",
        subject="Quick sync tomorrow?",
        body="Can we schedule a 30-minute sync tomorrow?",
        sender_name="Sarah Kim",
        sender_email="sarah.kim@company.com",
        available_slots=[
            CalendarSlot(slot_id="easy_slot_1", day="2026-04-02", start_time="10:00", end_time="10:30", is_available=True),
            CalendarSlot(slot_id="easy_slot_2", day="2026-04-02", start_time="14:00", end_time="14:30", is_available=True),
        ],
    ),

    EmailScenario(
        scenario_id="medium_001",
        task_level="medium",
        subject="Reschedule interview",
        body="I need to reschedule my interview.",
        sender_name="Alex Rivera",
        sender_email="alex@example.com",
        available_slots=[
            CalendarSlot(slot_id="medium_slot_1", day="2026-04-03", start_time="18:30", end_time="19:00", is_available=True),
        ],
    ),

    EmailScenario(
        scenario_id="hard_001",
        task_level="hard",
        subject="Urgent conflict",
        body="Board prep conflicts with investor call.",
        sender_name="Jordan Patel",
        sender_email="jordan@company.com",
        available_slots=[
            CalendarSlot(slot_id="hard_slot_1", day="2026-04-02", start_time="13:00", end_time="13:30", is_available=True),
        ],
    ),
]


GROUND_TRUTH = {
    "easy_001": {
        "triage_label": "meeting_request",
        "urgency": "medium",
        "intent": "schedule_meeting",
        "chosen_operation": "book_slot",
        "preferred_slot": "easy_slot_1",
    },
    "medium_001": {
        "triage_label": "reschedule_request",
        "urgency": "high",
        "intent": "reschedule_meeting",
        "chosen_operation": "propose_alternative",
    },
    "hard_001": {
        "triage_label": "urgent_escalation",
        "urgency": "critical",
        "intent": "reschedule_meeting",
        "chosen_operation": "propose_alternative",
    },
}