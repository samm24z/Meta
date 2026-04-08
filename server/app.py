from fastapi import FastAPI
import uvicorn

from server.test_env_environment import InboxOpsEnvironment


env = InboxOpsEnvironment()
app: FastAPI = env.app


@app.get("/")
def root():
    return {
        "name": "InboxOps Environment",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()