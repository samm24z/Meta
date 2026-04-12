FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn requests

ENV PYTHONPATH=/app

EXPOSE 8000

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]