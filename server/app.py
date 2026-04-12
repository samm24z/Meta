from fastapi import FastAPI
from server.test_env_environment import TestEnvironment

app = FastAPI()

env = TestEnvironment()


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    try:
        return env.reset()
    except Exception as e:
        return {"error": str(e)}


@app.post("/step")
def step(action: dict):
    try:
        return env.step(action)
    except Exception as e:
        return {"error": str(e)}