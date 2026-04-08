from openenv.core.env_server import create_app

from models import InboxAction, InboxObservation
from server.test_env_environment import TestEnvironment

app = create_app(
    TestEnvironment,
    InboxAction,
    InboxObservation,
)