from unittest.mock import patch
from schemas import TranscriptRead
from tests.data import TEST_HEADERS, TEST_USER_1_SUB, TEST_TRANSCRIPT_1, TEST_VIDEO_1


# Case: Invalid YouTube video ID
def test_get_transcript_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    invalid_video_id = "invalid_id"  # valid id has 11 symbols

    # ----------------- ACT ------------------
    response = client.get(f"/transcripts/{invalid_video_id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid YouTube video ID"}


# Case: Transcript exists in the db
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
    expected = TranscriptRead.model_validate(TEST_TRANSCRIPT_1)
    assert response.status_code == 200
    assert response.json() == expected.model_dump()


# Case: Transcript not found in the db
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
    assert response.json() == {
        "detail": "Video is not added yet. Please add the video first."
    }
