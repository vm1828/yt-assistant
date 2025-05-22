from unittest.mock import patch

from schemas import VideoResponse
from tests.data import *


# Case: Invalid YouTube Video ID
def test_get_user_video_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    invalid_video_id = "invalid_id"  # valid id has 11 symbols

    # ----------------- ACT ------------------
    response = client.get(f"/videos/{invalid_video_id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid YouTube video ID"}


# Case: User video exists in the account
@patch("api.routes.video.get_account_by_id_async")
@patch("api.routes.video.get_account_video")
@patch("api.routes.video.get_video")
@patch("api.routes.video.fetch_video_title")
@patch("api.routes.video.create_video")
@patch("api.routes.video.add_video_to_account")
def test_get_user_video_200_in_account(
    mock_add_video_to_account,
    mock_create_video,
    mock_fetch_video_title,
    mock_get_video,
    mock_get_account_video,
    mock_get_account_by_id_async,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    mock_get_account_by_id_async.return_value = TEST_ACCOUNT_1
    mock_get_account_video.return_value = TEST_VIDEO_1  # Video exists in account

    # ----------------- ACT ------------------
    response = client.get(f"/videos/{TEST_VIDEO_1.id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_async.call_count == 1
    assert mock_get_account_video.call_count == 1
    assert mock_get_video.call_count == 0
    assert mock_fetch_video_title.call_count == 0
    assert mock_create_video.call_count == 0
    assert mock_add_video_to_account.call_count == 0
    expected = VideoResponse.model_validate(TEST_VIDEO_1)
    assert response.status_code == 200
    assert response.json() == expected.model_dump()


# Case: Video not in the account, not in the db, but can be fetched from YouTube
@patch("api.routes.video.get_account_by_id_async")
@patch("api.routes.video.get_account_video")
@patch("api.routes.video.get_video")
@patch("api.routes.video.fetch_video_transcript")
@patch("api.routes.video.fetch_video_title")
@patch("api.routes.video.create_video")
@patch("api.routes.video.add_video_to_account")
def test_get_user_video_200_creates_video_from_youtube(
    mock_add_video_to_account,
    mock_create_video,
    mock_fetch_video_title,
    mock_fetch_video_transcript,
    mock_get_video,
    mock_get_account_video,
    mock_get_account_by_id_async,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    mock_get_account_by_id_async.return_value = TEST_ACCOUNT_1
    mock_get_account_video.return_value = None  # Video doesn't exist in account
    mock_get_video.return_value = None  # Video doesn't exist in db
    mock_fetch_video_title.return_value = "YouTube Video Title"
    mock_fetch_video_transcript.return_value = "Youtube Video Transcript"
    mock_create_video.return_value = (
        TEST_VIDEO_1  # Video will be created in the account
    )

    # ----------------- ACT ------------------
    response = client.get(f"/videos/{TEST_VIDEO_1.id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_async.call_count == 1
    assert mock_get_account_video.call_count == 1
    assert mock_get_video.call_count == 1
    assert mock_fetch_video_title.call_count == 1
    assert mock_fetch_video_transcript.call_count == 1
    assert mock_create_video.call_count == 1
    assert mock_add_video_to_account.call_count == 0
    expected = VideoResponse.model_validate(TEST_VIDEO_1)
    assert response.status_code == 200
    assert response.json() == expected.model_dump()


# Case: Video not in the account, not in the db, not found on YouTube
@patch("api.routes.video.get_account_by_id_async")
@patch("api.routes.video.get_account_video")
@patch("api.routes.video.get_video")
@patch("api.routes.video.fetch_video_transcript")
@patch("api.routes.video.fetch_video_title")
@patch("api.routes.video.create_video")
@patch("api.routes.video.add_video_to_account")
def test_get_user_video_404_not_in_db_not_in_youtube(
    mock_add_video_to_account,
    mock_create_video,
    mock_fetch_video_title,
    mock_fetch_video_transcript,
    mock_get_video,
    mock_get_account_video,
    mock_get_account_by_id_async,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    mock_get_account_by_id_async.return_value = TEST_ACCOUNT_1
    mock_get_account_video.return_value = None  # Video doesn't exist in account
    mock_get_video.return_value = None  # Video doesn't exist in db
    mock_fetch_video_title.return_value = None  # YouTube title fetch failed
    mock_fetch_video_transcript.return_value = None  # Transcript fetch failed

    # ----------------- ACT ------------------
    response = client.get(f"/videos/{TEST_VIDEO_1.id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_async.call_count == 1
    assert mock_get_account_video.call_count == 1
    assert mock_get_video.call_count == 1
    assert mock_fetch_video_title.call_count == 1
    assert mock_fetch_video_title.call_count == 1
    assert mock_create_video.call_count == 0
    assert mock_add_video_to_account.call_count == 0
    assert mock_add_video_to_account.call_count == 0
    assert response.status_code == 404
    assert response.json() == {"detail": "Video not found or without a transcript."}


# Case: Video not in the account, but in db
@patch("api.routes.video.get_account_by_id_async")
@patch("api.routes.video.get_account_video")
@patch("api.routes.video.get_video")
@patch("api.routes.video.fetch_video_transcript")
@patch("api.routes.video.fetch_video_title")
@patch("api.routes.video.create_video")
@patch("api.routes.video.add_video_to_account")
def test_get_user_video_200_in_db_adds_to_account(
    mock_add_video_to_account,
    mock_create_video,
    mock_fetch_video_transcript,
    mock_fetch_video_title,
    mock_get_video,
    mock_get_account_video,
    mock_get_account_by_id_async,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_by_id_async.return_value = TEST_ACCOUNT_1
    mock_get_account_video.return_value = None  # Video doesn't exist in account
    mock_get_video.return_value = TEST_VIDEO_1  # Video already in the db
    mock_add_video_to_account.return_value = None  # Video is added to the account

    # ----------------- ACT ------------------
    response = client.get(f"/videos/{TEST_VIDEO_1.id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_by_id_async.call_count == 1
    assert mock_get_account_video.call_count == 1
    assert mock_get_video.call_count == 1
    assert mock_fetch_video_title.call_count == 0
    assert mock_fetch_video_transcript.call_count == 0
    assert mock_create_video.call_count == 0
    assert mock_add_video_to_account.call_count == 1
    expected = VideoResponse.model_validate(TEST_VIDEO_1)
    assert response.status_code == 200
    assert response.json() == expected.model_dump()
