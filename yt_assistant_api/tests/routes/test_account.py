from unittest.mock import patch
from fastapi import HTTPException, status

from main import app
from models import Account
from tests.data import *


# Case: No account exists, create one
@patch("api.routes.account.get_account_by_id_sync")
@patch("api.routes.account.create_account")
def test_get_authenticated_user_200_creates_account_if_missing(
    mock_create_account, mock_get_account_by_id_sync, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_sync.return_value = None
    mock_create_account.return_value = Account(id=TEST_USER_1_SUB)

    # ----------------- ACT ------------------
    response = client.get("/accounts/me", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_sync.call_count == 1
    assert mock_create_account.call_count == 1
    assert response.status_code == 200
    assert response.json() == {"id": TEST_USER_1_SUB}


# Case: Account exists already, return it
@patch("api.routes.account.get_account_by_id_sync")
@patch("api.routes.account.create_account")
def test_get_authenticated_user_200_returns_existing_account(
    mock_create_account, mock_get_account_by_id_sync, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_sync.return_value = Account(id=TEST_USER_1_SUB)

    # ----------------- ACT ------------------
    response = client.get("/accounts/me", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_sync.call_count == 1
    assert mock_create_account.call_count == 0
    assert response.status_code == 200
    assert response.json() == {"id": TEST_USER_1_SUB}


# Case: Unauthorized access with invalid token
@patch("core.auth.verify_jwt_token")
def test_get_authenticated_user_401_rejects_unauthorized_request(
    mock_verify_jwt_token, client_factory
):
    # ---------------- ARRANGE ----------------
    unauthenticated_client = client_factory("asdf", auth=False)
    headers = {"Authorization": "Bearer invalid_token"}

    # mock_get_jwk.return_value = {}
    mock_verify_jwt_token.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )

    # ----------------- ACT ------------------
    response = unauthenticated_client.get("/accounts/me", headers=headers)

    # ---------------- ASSERT ----------------
    assert mock_verify_jwt_token.call_count == 1
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


# Case: Unauthorized access with missing Authorization header
@patch("core.auth.verify_jwt_token")
def test_get_authenticated_user_401_missing_auth_header(
    mock_verify_jwt_token, client_factory
):
    # ----------------- ACT ------------------
    unauthenticated_client = client_factory("asdf", auth=False)
    response = unauthenticated_client.get("/accounts/me")

    # ---------------- ASSERT ----------------
    # Token verification shouldn't even be called
    assert mock_verify_jwt_token.call_count == 0
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
