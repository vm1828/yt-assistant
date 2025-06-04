from unittest.mock import patch

from models import Video
from schemas import VideoResponse
from tests.data import *

# =========================================== GET ===========================================


# Case 200: Video found in the account
@patch("api.routes.video.get_account_video")
def test_get_user_video_200(mock_get_account_video, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_account_video.return_value = TEST_VIDEO_1

    # ----------------- ACT ------------------
    response = client.get(f"/videos/{TEST_VIDEO_1.id}", headers=TEST_HEADERS)
    expected = VideoResponse.model_validate(TEST_VIDEO_1)

    # ---------------- ASSERT ----------------
    assert mock_get_account_video.call_count == 1
    assert response.status_code == 200
    assert response.json() == expected.model_dump()


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


# Case 404: Video not found in the account
@patch("api.routes.video.get_account_video")
def test_get_user_video_404_video_not_found(mock_get_account_video, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    valid_video_id = 11111111111
    mock_get_account_video.return_value = None

    # ----------------- ACT ------------------
    response = client.get(f"/videos/{valid_video_id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_get_account_video.call_count == 1
    assert response.status_code == 404
    assert response.json() == {"detail": "Video not found for this user"}


# =========================================== POST ===========================================


# Case 201: Video in db and can be added to the account
@patch("api.routes.video.add_video_to_account")
@patch("api.routes.video.get_video")
def test_post_user_video_201_video_in_db_can_be_added_to_account(
    mock_get_video,
    mock_add_video_to_account,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_video.return_value = TEST_VIDEO_1

    # ----------------- ACT ------------------
    response = client.post(
        "/videos/",
        headers=TEST_HEADERS,
        json={"id": TEST_VIDEO_1.id},
    )
    expected = VideoResponse.model_validate(TEST_VIDEO_1)

    # ---------------- ASSERT ----------------
    assert mock_get_video.call_count == 1
    assert mock_add_video_to_account.call_count == 1
    assert response.status_code == 201
    assert response.json() == expected.model_dump()


# Case 201: Video not in db, but can be fetched from YouTube
@patch("api.routes.video.create_video")
@patch("api.routes.video.fetch_video_transcript")
@patch("api.routes.video.fetch_video_title")
@patch("api.routes.video.get_video")
def test_post_user_video_201_video_not_in_db_can_be_fetched(
    mock_get_video,
    mock_fetch_video_title,
    mock_fetch_video_transcript,
    mock_create_video,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_video.return_value = None
    mock_fetch_video_title.return_value = TEST_VIDEO_1.title
    mock_fetch_video_transcript.return_value = "video_transcript"
    mock_create_video.return_value = TEST_VIDEO_1

    # ----------------- ACT ------------------
    response = client.post(
        "/videos/",
        headers=TEST_HEADERS,
        json={"id": TEST_VIDEO_1.id},
    )
    expected = VideoResponse.model_validate(TEST_VIDEO_1)

    # ---------------- ASSERT ----------------
    assert mock_get_video.call_count == 1
    assert mock_fetch_video_title.call_count == 1
    assert mock_fetch_video_transcript.call_count == 1
    assert mock_create_video.call_count == 1
    assert response.status_code == 201
    assert response.json() == expected.model_dump()


# Case 400: Invalid YouTube Video ID
def test_post_user_video_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    invalid_video_id = "invalid_id"  # valid id has 11 symbols

    # ----------------- ACT ------------------
    response = client.post(
        "/videos/",
        headers=TEST_HEADERS,
        json={"id": invalid_video_id},
    )

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid YouTube video ID"}


# Case 409: Video in db and already added to the account
@patch("api.routes.video.add_video_to_account")
@patch("api.routes.video.get_video")
def test_post_user_video_409_video_in_db_already_added_to_account(
    mock_get_video,
    mock_add_video_to_account,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    video = Video(id=TEST_VIDEO_1.id, title=TEST_VIDEO_1.title)
    video.account_videos = [TEST_ACCOUNT_1_VIDEO_1]
    mock_get_video.return_value = video

    # ----------------- ACT ------------------
    response = client.post(
        "/videos/",
        headers=TEST_HEADERS,
        json={"id": TEST_VIDEO_1.id},
    )

    # ---------------- ASSERT ----------------
    assert mock_get_video.call_count == 1
    assert mock_add_video_to_account.call_count == 0
    assert response.status_code == 409
    assert response.json() == {"detail": "Video already added to the account"}


# Case 404: Video not in db and does not exist
@patch("api.routes.video.create_video")
@patch("api.routes.video.fetch_video_transcript")
@patch("api.routes.video.fetch_video_title")
@patch("api.routes.video.get_video")
def test_post_user_video_404_video_not_in_db_no_title(
    mock_get_video,
    mock_fetch_video_title,
    mock_fetch_video_transcript,
    mock_create_video,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    valid_video_id = "11111111111"
    mock_get_video.return_value = None
    mock_fetch_video_title.return_value = None
    mock_fetch_video_transcript.return_value = "asdf"

    # ----------------- ACT ------------------
    response = client.post(
        "/videos/",
        headers=TEST_HEADERS,
        json={"id": valid_video_id},
    )

    # ---------------- ASSERT ----------------
    assert mock_get_video.call_count == 1
    assert mock_fetch_video_title.call_count == 1
    assert mock_fetch_video_transcript.call_count == 1
    assert mock_create_video.call_count == 0
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Video not found or failed to fetch a transcript"
    }


# Case 404: Video not in db and without a transcript
@patch("api.routes.video.create_video")
@patch("api.routes.video.fetch_video_transcript")
@patch("api.routes.video.fetch_video_title")
@patch("api.routes.video.get_video")
def test_post_user_video_404_video_not_in_db_no_transcript(
    mock_get_video,
    mock_fetch_video_title,
    mock_fetch_video_transcript,
    mock_create_video,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    valid_video_id = "11111111111"
    mock_get_video.return_value = None
    mock_fetch_video_title.return_value = "video title"
    mock_fetch_video_transcript.return_value = None

    # ----------------- ACT ------------------
    response = client.post(
        "/videos/",
        headers=TEST_HEADERS,
        json={"id": valid_video_id},
    )

    # ---------------- ASSERT ----------------
    assert mock_get_video.call_count == 1
    assert mock_fetch_video_title.call_count == 1
    assert mock_fetch_video_transcript.call_count == 1
    assert mock_create_video.call_count == 0
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Video not found or failed to fetch a transcript"
    }
