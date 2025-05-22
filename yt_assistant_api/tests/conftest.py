import os
import pytest

from fastapi.testclient import TestClient
from main import app

from core import get_current_account
from schemas import Auth0Payload


@pytest.fixture(scope="session", autouse=True)
def set_local_env():
    # Set env vars
    env_vars = {
        "POSTGRES_URL": "",
        "GOOGLE_API_KEY": "",
    }
    original_env = {key: os.environ.get(key) for key in env_vars}
    os.environ.update(env_vars)

    yield

    # Restore original env
    for key in env_vars:
        if original_env[key] is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_env[key]


@pytest.fixture
def client_factory():
    def make_client(sub: str, auth=True):
        if not auth:
            return TestClient(app)
        app.dependency_overrides[get_current_account] = lambda: Auth0Payload(sub=sub)
        client = TestClient(app)
        return client

    yield make_client
    app.dependency_overrides.clear()
