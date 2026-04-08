from openenv.core.env_server import create_app
import uvicorn

from server.test_env_environment import TestEnvironment
from models import InboxAction, InboxObservation


app = create_app(TestEnvironment, InboxAction, InboxObservation)


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()