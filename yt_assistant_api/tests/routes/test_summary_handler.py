from unittest.mock import patch, MagicMock

from tests.data import (
    TEST_USER_1_SUB,
    TEST_HEADERS,
    TEST_TRANSCRIPT_1,
    TEST_SUMMARY_1,
)


# Case: Unauthorized (no token)
def test_get_video_summary_401_unauthorized(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB, auth=False)

    # ----------------- ACT ------------------
    response = client.get(f"/summaries/{TEST_TRANSCRIPT_1.video_id}")

    # ---------------- ASSERT ----------------
    assert response.status_code == 401


# Case: Invalid YouTube Video ID
def test_get_video_summary_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    invalid_video_id = "bad_id"  # valid id has 11 symbols

    # ----------------- ACT ------------------
    response = client.get(f"/summaries/{invalid_video_id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid YouTube video ID"}


# Case: Transcript not found
@patch("api.routes.summary.create_summary")
@patch("api.routes.summary.summarize")
@patch("api.routes.summary.get_summary")
@patch("api.routes.summary.get_transcript")
@patch("api.routes.summary.validate_video_id")
def test_get_video_summary_404_no_transcript(
    mock_validate_video_id,
    mock_get_transcript,
    mock_get_summary,
    mock_summarize,
    mock_create_summary,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_transcript.return_value = None

    # ----------------- ACT ------------------
    response = client.get(
        f"/summaries/{TEST_TRANSCRIPT_1.video_id}", headers=TEST_HEADERS
    )

    # ---------------- ASSERT ----------------
    assert mock_validate_video_id.call_count == 1
    assert mock_get_transcript.call_count == 1
    assert mock_get_summary.call_count == 0
    assert mock_summarize.call_count == 0
    assert mock_create_summary.call_count == 0
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Video is not added yet. Please add the video first."
    }


# Case: Summary already exists
@patch("api.routes.summary.create_summary")
@patch("api.routes.summary.summarize")
@patch("api.routes.summary.get_summary")
@patch("api.routes.summary.get_transcript")
@patch("api.routes.summary.validate_video_id")
def test_get_video_summary_200_existing_summary(
    mock_validate_video_id,
    mock_get_transcript,
    mock_get_summary,
    mock_summarize,
    mock_create_summary,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    # transcript exists
    mock_get_transcript.return_value = TEST_TRANSCRIPT_1
    # summary already in db
    mock_summary = MagicMock(summary_text=TEST_SUMMARY_1.summary_text)
    mock_get_summary.return_value = mock_summary

    # ----------------- ACT ------------------
    response = client.get(
        f"/summaries/{TEST_TRANSCRIPT_1.video_id}", headers=TEST_HEADERS
    )

    # ---------------- ASSERT ----------------
    assert mock_validate_video_id.call_count == 1
    assert mock_get_transcript.call_count == 1
    assert mock_get_summary.call_count == 1
    assert mock_summarize.call_count == 0
    assert mock_create_summary.call_count == 0
    assert response.status_code == 200
    assert response.json() == {
        "video_id": TEST_TRANSCRIPT_1.video_id,
        "summary_text": TEST_SUMMARY_1.summary_text,
    }


# Case: Creates new summary when none exists
@patch("api.routes.summary.create_summary")
@patch("api.routes.summary.summarize")
@patch("api.routes.summary.get_summary")
@patch("api.routes.summary.get_transcript")
@patch("api.routes.summary.validate_video_id")
def test_get_video_summary_200_creates_summary(
    mock_validate_video_id,
    mock_get_transcript,
    mock_get_summary,
    mock_summarize,
    mock_create_summary,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    # transcript exists
    mock_get_transcript.return_value = TEST_TRANSCRIPT_1
    # no summary yet
    mock_get_summary.return_value = None
    # LLM returns text
    generated = TEST_SUMMARY_1.summary_text
    mock_summarize.return_value = generated
    # DB returns saved summary
    saved = MagicMock(summary_text=generated)
    mock_create_summary.return_value = saved

    # ----------------- ACT ------------------
    response = client.get(
        f"/summaries/{TEST_TRANSCRIPT_1.video_id}", headers=TEST_HEADERS
    )

    # ---------------- ASSERT ----------------
    assert mock_validate_video_id.call_count == 1
    assert mock_get_transcript.call_count == 1
    assert mock_get_summary.call_count == 1
    assert mock_summarize.call_count == 1
    assert mock_create_summary.call_count == 1
    assert response.status_code == 200
    assert response.json() == {
        "video_id": TEST_TRANSCRIPT_1.video_id,
        "summary_text": generated,
    }
