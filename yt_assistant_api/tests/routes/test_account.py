from unittest.mock import patch
from fastapi import HTTPException, status

from main import app
from models.account import Account
from tests.data.account import TEST_USER_SUB


# Case 1: No account exists, create one
@patch("api.routes.account.get_account_by_id")
@patch("api.routes.account.create_account")
def test_get_authenticated_user_creates_account_if_missing(
    mock_create_account, mock_get_account_by_id, client
):
    # ---------------- ARRANGE ----------------

    mock_get_account_by_id.return_value = None
    mock_create_account.return_value = Account(id=TEST_USER_SUB)

    # ----------------- ACT ------------------
    response = client.get(
        "/accounts/me", headers={"Authorization": "Bearer test_token"}
    )

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id.call_count == 1
    assert mock_create_account.call_count == 1
    assert response.status_code == 200
    assert response.json() == {"id": TEST_USER_SUB}


# Case 2: Account exists already, return it
@patch("api.routes.account.get_account_by_id")
@patch("api.routes.account.create_account")
def test_get_authenticated_user_returns_existing_account(
    mock_create_account, mock_get_account_by_id, client
):
    # ---------------- ARRANGE ----------------

    mock_get_account_by_id.return_value = Account(id=TEST_USER_SUB)

    # ----------------- ACT ------------------
    response = client.get(
        "/accounts/me", headers={"Authorization": "Bearer test_token"}
    )

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id.call_count == 1
    assert mock_create_account.call_count == 0
    assert response.status_code == 200
    assert response.json() == {"id": TEST_USER_SUB}


# Case 3: Unauthorized access with invalid token
@patch("core.auth.verify_jwt_token")
def test_get_authenticated_user_rejects_unauthorized_request(
    mock_verify_jwt_token, unauthenticated_client
):
    # ---------------- ARRANGE ----------------
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


# Case 4: Unauthorized access with missing Authorization header
@patch("core.auth.verify_jwt_token")
def test_get_authenticated_user_missing_auth_header(
    mock_verify_jwt_token, unauthenticated_client
):
    # ----------------- ACT ------------------
    response = unauthenticated_client.get("/accounts/me")

    # ---------------- ASSERT ----------------
    # Token verification shouldn't even be called
    assert mock_verify_jwt_token.call_count == 0
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
