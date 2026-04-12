FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

# 👇 CRITICAL FIX (keeps container alive)
CMD uvicorn server.app:app --host 0.0.0.0 --port 8000