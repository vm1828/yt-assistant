from unittest.mock import patch

# from fastapi import HTTPException, status

from schemas import VideosResponse
from tests.data import *


# Case 1: User has videos
@patch("api.routes.video.get_account_by_id_async")
def test_get_user_videos_returns_user_videos(
    mock_get_account_by_id_async, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_async.return_value = TEST_ACCOUNT_1

    # ----------------- ACT ------------------
    response = client.get("/videos/", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    expected = VideosResponse.model_validate({"videos": [TEST_VIDEO_1, TEST_VIDEO_2]})
    assert response.status_code == 200
    assert response.json() == expected.model_dump()


# Case 2: User has no videos
@patch("api.routes.video.get_account_by_id_async")
def test_get_user_videos_returns_empty_list_if_no_videos(
    mock_get_account_by_id_async, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_async.return_value = Account(
        id="test_user_no_videos", account_videos=[]
    )

    # ----------------- ACT ------------------
    response = client.get("/videos/", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert response.status_code == 200
    assert response.json() == {"videos": []}
