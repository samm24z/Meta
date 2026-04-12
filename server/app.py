from fastapi import FastAPI
from server.test_env_environment import TestEnvironment

app = FastAPI()

env = TestEnvironment()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(action: dict):
    return env.step(action)