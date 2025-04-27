import pytest
from fastapi.testclient import TestClient
from main import app
from core.auth import get_current_account
from schemas.account import Auth0Payload
from tests.data.account import TEST_USER_SUB


@pytest.fixture
def client():
    app.dependency_overrides[get_current_account] = lambda: Auth0Payload(
        sub=TEST_USER_SUB
    )

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def unauthenticated_client():
    yield TestClient(app)
