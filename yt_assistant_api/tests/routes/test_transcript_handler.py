from unittest.mock import patch

from core.exceptions import EXC_400_INVALID_YT_ID, EXC_404_VID_NOT_ADDED
from schemas import TranscriptResponse
from tests.data import TEST_HEADERS, TEST_TRANSCRIPT_1, TEST_USER_1_SUB, TEST_VIDEO_1


# Case 200: Transcript exists in the db
@patch("api.routes.transcript.get_transcript")
@patch("api.routes.transcript.validate_video_id")
def test_get_transcript_200(
    mock_validate_video_id,
    mock_get_transcript,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    mock_get_transcript.return_value = TEST_TRANSCRIPT_1

    # ----------------- ACT ------------------
    response = client.get(f"/transcripts/{TEST_VIDEO_1.id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_validate_video_id.call_count == 1
    assert mock_get_transcript.call_count == 1
    expected = TranscriptResponse.model_validate(TEST_TRANSCRIPT_1)
    assert response.status_code == 200
    assert response.json() == expected.model_dump()


# Case 400: Invalid YouTube video ID
def test_get_transcript_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    invalid_video_id = "invalid_id"  # valid id has 11 symbols

    # ----------------- ACT ------------------
    response = client.get(f"/transcripts/{invalid_video_id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json()["detail"] == EXC_400_INVALID_YT_ID.detail


# Case 404: Transcript not found in the db
@patch("api.routes.transcript.get_transcript")
@patch("api.routes.transcript.validate_video_id")
def test_get_transcript_404_not_found(
    mock_validate_video_id,
    mock_get_transcript,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    mock_validate_video_id.return_value = None
    mock_get_transcript.return_value = None

    # ----------------- ACT ------------------
    response = client.get("/transcripts/abcdefghijk", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert mock_validate_video_id.call_count == 1
    assert mock_get_transcript.call_count == 1
    assert response.status_code == 404
    assert response.json()["detail"] == EXC_404_VID_NOT_ADDED.detail
