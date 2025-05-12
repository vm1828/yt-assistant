import os
import pytest

from fastapi.testclient import TestClient
from main import app

from core import get_current_account
from schemas import Auth0Payload


@pytest.fixture(scope="session", autouse=True)
def set_local_env():
    os.environ["POSTGRES_URL"] = ""
    yield
    del os.environ["POSTGRES_URL"]


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
