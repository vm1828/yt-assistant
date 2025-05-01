from unittest.mock import patch, MagicMock

# from fastapi import HTTPException, status

from schemas import VideoReadList
from tests.data import *


# Case 1: User has videos -> return them
@patch("api.routes.video.get_account_by_id")
def test_get_user_videos_returns_user_videos(mock_get_account_by_id, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id.return_value = TEST_ACCOUNT_1

    # ----------------- ACT ------------------
    response = client.get("/videos/", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    expected = VideoReadList.model_validate({"videos": [TEST_VIDEO_1, TEST_VIDEO_2]})
    assert response.status_code == 200
    assert response.json() == expected.model_dump()


# Case 2: User has no videos -> 404
@patch("api.routes.video.get_account_by_id")
def test_get_user_videos_returns_404_if_no_videos(
    mock_get_account_by_id, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id.return_value = Account(
        id="test_user_no_videos", account_videos=[]
    )

    # ----------------- ACT ------------------
    response = client.get("/videos/", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert response.status_code == 404
    assert response.json() == {"detail": "No videos found for this user."}
