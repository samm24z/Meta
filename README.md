---
title: InboxOps Environment
emoji: 📬
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# InboxOps Environment

InboxOps is a real-world **OpenEnv reinforcement learning environment** for **email triage, scheduling, and response drafting**.

It simulates realistic inbox assistant workflows where an AI agent must:

1. **Understand incoming emails**
2. **Classify intent and urgency**
3. **Take the correct operational action**
4. **Draft a useful response**

This environment is designed for **agent evaluation, reinforcement learning research, and practical workflow automation benchmarking**.

---

## 🚀 What the Environment Does

Each episode presents an email-based task such as:

- meeting scheduling
- rescheduling requests
- urgent escalations
- follow-ups
- availability checks

The agent interacts using the standard OpenEnv-style API:

- `reset()`
- `step(action)`
- `state`

and is evaluated across:

- **triage quality**
- **decision correctness**
- **response drafting quality**

---

## 🧠 Task Structure

Each task is structured into **three progressive steps**:

### Step 1 — Triage
The agent must classify the email:

- `triage_label`
- `urgency`
- `intent`

### Step 2 — Operational Decision
The agent chooses the appropriate action:

- `book_slot`
- `decline`
- `propose_alternative`
- `escalate`
- `request_more_info`
- `no_action_needed`

### Step 3 — Draft Response
The agent produces a final response draft.

---

## 📦 Included Features

- ✅ OpenEnv-compatible FastAPI server
- ✅ Typed Pydantic action / observation schemas
- ✅ 3+ deterministic graded tasks
- ✅ Reward shaping and partial scoring
- ✅ Hugging Face Space deployment support
- ✅ Docker-based deployment
- ✅ Reproducible baseline inference script
- ✅ Structured logging for evaluation

---

## 🗂 Project Structure

```bash
.
├── inference.py
├── models.py
├── graders.py
├── sample_data.py
├── openenv.yaml
├── README.md
├── Dockerfile
├── requirements.txt
└── server/
    ├── app.py
    └── test_env_environment.py
```

---

## 🔁 API Overview

### `POST /reset`
Starts a new episode and returns the first observation.

### `POST /step`
Takes a structured action and returns:

- next observation
- reward
- done flag

### `GET /health`
Health check endpoint for deployment validation.

### `GET /docs`
Swagger UI for testing the environment.

---

## 🧾 Action Schema

The agent acts using a structured `InboxAction` object:

```json
{
  "triage_label": "meeting_request",
  "urgency": "medium",
  "intent": "schedule_meeting",
  "chosen_operation": "book_slot",
  "selected_slot": "easy_slot_1",
  "reason": "Selected earliest valid slot.",
  "response_draft": "Hi Sarah, thanks for reaching out..."
}
```

---

## 👀 Observation Schema

Each observation contains:

- email subject and body
- sender details
- thread history
- available calendar slots
- valid slot IDs
- task ID
- partial evaluation signals

This allows agents to reason over both **language** and **structured scheduling state**.

---

## 🏆 Reward & Evaluation

The environment uses **task-specific graders** to score actions across:

- **triage accuracy**
- **scheduling correctness**
- **response draft quality**

Scores are normalized to the **0.0–1.0** range and exposed as:

- `triage_score`
- `operation_score`
- `draft_score`

Reward shaping is also included to make the environment useful for RL training loops.

---

## 📊 Included Tasks

This environment includes at least **3 graded tasks**:

- `easy_001`
- `medium_001`
- `hard_001`

Each task has deterministic scenario setup and grading logic.

---

## 🤖 Baseline Inference

A reproducible baseline is provided in:

```bash
inference.py
```

It uses the required environment variables:

- `API_BASE_URL`
- `MODEL_NAME`
- `HF_TOKEN`

and emits structured logs in the required format:

- `[START]`
- `[STEP]`
- `[END]`

---

## ⚙️ Run Locally

### 1) Install dependencies
```bash
uv sync
```

### 2) Start the environment server
```bash
uv run uvicorn server.app:app --host 0.0.0.0 --port 8000
```

### 3) Test the API
Open:

```bash
http://127.0.0.1:8000/docs
```

### 4) Run baseline inference
```bash
uv run python inference.py
```

---

## ✅ Validation

Run OpenEnv validation locally:

```bash
uv run openenv validate
```

Expected output:

```bash
[OK] test: Ready for multi-mode deployment
```

---

## 🐳 Docker

Build locally:

```bash
docker build -t inboxops-env .
```

Run:

```bash
docker run -p 8000:7860 inboxops-env
```

---

## 🌐 Deployment

This environment is deployed as a **Hugging Face Space** and is accessible through its hosted API endpoints.

---

## 📌 Why This Environment Matters

InboxOps is useful because it benchmarks an agent’s ability to:

- interpret user intent
- make structured operational decisions
- handle scheduling constraints
- communicate clearly in natural language

This makes it a practical environment for:

- RL benchmarking
- agent evaluation
- workflow automation research
- assistant training

---

## 📜 License

This project is intended for educational and hackathon submission purposes.