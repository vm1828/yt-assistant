from unittest.mock import patch
from fastapi import HTTPException, status

from main import app
from models import Account
from tests.data import *

# =========================================== GET ===========================================


# Case: No account exists, return 404
@patch("api.routes.account.get_account_by_id_sync")
def test_get_authenticated_user_404_if_account_missing(
    mock_get_account_by_id_sync, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_sync.return_value = None

    # ----------------- ACT ------------------
    response = client.get("/accounts/", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_sync.call_count == 1
    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found"}


# Case: Account exists already, return it
@patch("api.routes.account.get_account_by_id_sync")
def test_get_authenticated_user_200_returns_existing_account(
    mock_get_account_by_id_sync, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_sync.return_value = Account(id=TEST_USER_1_SUB)

    # ----------------- ACT ------------------
    response = client.get("/accounts/", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_sync.call_count == 1
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
    response = unauthenticated_client.get("/accounts/", headers=headers)

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
    response = unauthenticated_client.get("/accounts/")

    # ---------------- ASSERT ----------------
    # Token verification shouldn't even be called
    assert mock_verify_jwt_token.call_count == 0
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


# =========================================== POST ===========================================


# Case: Account does not exist, create it
@patch("api.routes.account.get_account_by_id_sync")
@patch("api.routes.account.create_account")
def test_post_authenticated_user_201_creates_account(
    mock_create_account, mock_get_account_by_id_sync, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_sync.return_value = None
    mock_create_account.return_value = Account(id=TEST_USER_1_SUB)

    # ----------------- ACT ------------------
    response = client.post("/accounts/", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_sync.call_count == 1
    assert mock_create_account.call_count == 1
    assert response.status_code == 200
    assert response.json() == {"id": TEST_USER_1_SUB}


# Case: Account already exists, return 409
@patch("api.routes.account.get_account_by_id_sync")
@patch("api.routes.account.create_account")
def test_post_authenticated_user_409_if_account_exists(
    mock_create_account, mock_get_account_by_id_sync, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_sync.return_value = Account(id=TEST_USER_1_SUB)

    # ----------------- ACT ------------------
    response = client.post("/accounts/", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_sync.call_count == 1
    assert mock_create_account.call_count == 0
    assert response.status_code == 409
    assert response.json() == {"detail": "Account already exists"}


# Case: Unauthorized access with invalid token
@patch("core.auth.verify_jwt_token")
def test_post_authenticated_user_401_invalid_token(
    mock_verify_jwt_token, client_factory
):
    # ---------------- ARRANGE ----------------
    unauthenticated_client = client_factory("asdf", auth=False)
    headers = {"Authorization": "Bearer invalid_token"}

    mock_verify_jwt_token.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )

    # ----------------- ACT ------------------
    response = unauthenticated_client.post("/accounts/", headers=headers)

    # ---------------- ASSERT ----------------
    assert mock_verify_jwt_token.call_count == 1
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


# Case: Unauthorized access with missing Authorization header
@patch("core.auth.verify_jwt_token")
def test_post_authenticated_user_401_missing_auth_header(
    mock_verify_jwt_token, client_factory
):
    # ----------------- ACT ------------------
    unauthenticated_client = client_factory("asdf", auth=False)
    response = unauthenticated_client.post("/accounts/")

    # ---------------- ASSERT ----------------
    assert mock_verify_jwt_token.call_count == 0
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
