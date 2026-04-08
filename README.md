# InboxOps Environment

InboxOps is a reinforcement learning environment built with OpenEnv for email triage, meeting scheduling, and professional response drafting.

It simulates realistic inbox-management tasks where an agent must:

- classify incoming email intent
- determine urgency
- choose the correct scheduling / operational action
- draft an appropriate response

This environment is designed for training and evaluating agents through the standard OpenEnv API:

- `reset()`
- `step(action)`
- `state()`

---

# Why this environment?

Modern AI assistants increasingly need to operate on semi-structured workplace tasks such as:

- meeting requests
- rescheduling
- urgent calendar conflicts
- follow-ups
- inbox prioritization

InboxOps turns this into a learnable RL environment with structured observations, typed actions, deterministic grading, and reward shaping.

---

# Environment Overview

Each episode presents the agent with an email scenario that includes:

- email subject and body
- sender identity and role
- thread history
- available calendar slots
- policy notes / scheduling context

The agent must output a structured action describing how it would handle the request.

---

# Task Types

The environment currently includes multiple task difficulties:

- `easy_001` — straightforward scheduling request
- `medium_001` — reschedule scenario with moderate complexity
- `hard_001` — urgent scheduling conflict requiring higher-priority handling

Each task is scored using deterministic graders.

---

# RL Formulation

## Observation
The observation contains:

- current email scenario
- available calendar slots
- task metadata
- partial score feedback
- step number

## Action
The action contains:

- `triage_label`
- `urgency`
- `intent`
- `chosen_operation`
- `selected_slot`
- `reason`
- `response_draft`

## Reward
Reward is shaped using partial credit for:

- correct triage classification
- correct scheduling / operational decision
- acceptable response completion

Scores are normalized to the `0.0–1.0` range.

---

# Project Structure

```text
.
├── server/
│   ├── app.py
│   ├── test_env_environment.py
│   ├── Dockerfile
│   └── requirements.txt
├── models.py
├── sample_data.py
├── graders.py
├── inference.py
├── openenv.yaml
├── pyproject.toml
├── README.md
└── __init__.py