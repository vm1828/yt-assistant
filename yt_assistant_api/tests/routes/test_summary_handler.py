from unittest.mock import patch

from tests.data import (
    TEST_USER_1_SUB,
    TEST_HEADERS,
    TEST_TRANSCRIPT_1,
    TEST_SUMMARY_1,
)

# =========================================== GET ===========================================


# Case 200: Summary exists
@patch("api.routes.summary.get_summary")
@patch("api.routes.summary.get_transcript")
def test_get_video_summary_200(mock_get_transcript, mock_get_summary, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_transcript.return_value = TEST_TRANSCRIPT_1
    mock_get_summary.return_value = TEST_SUMMARY_1

    # ----------------- ACT ------------------
    response = client.get(
        f"/summaries/{TEST_TRANSCRIPT_1.video_id}", headers=TEST_HEADERS
    )
    expected = {
        "video_id": TEST_TRANSCRIPT_1.video_id,
        "summary_text": TEST_SUMMARY_1.summary_text,
    }

    # ---------------- ASSERT ----------------
    assert response.status_code == 200
    assert response.json() == expected


# Case 400: Invalid YouTube Video ID
def test_get_video_summary_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    invalid_video_id = "bad_id"  # valid id has 11 symbols

    # ----------------- ACT ------------------
    response = client.get(f"/summaries/{invalid_video_id}", headers=TEST_HEADERS)

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid YouTube video ID"}


# Case 401: Unauthorized
def test_get_video_summary_401_unauthorized(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB, auth=False)

    # ----------------- ACT ------------------
    response = client.get(f"/summaries/{TEST_TRANSCRIPT_1.video_id}")

    # ---------------- ASSERT ----------------
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


# Case 404: No transcript
@patch("api.routes.summary.get_transcript")
def test_get_video_summary_404_no_transcript(
    mock_get_transcript,
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
    assert mock_get_transcript.call_count == 1
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Video is not added yet. Please add the video first."
    }


# Case 404: Summary not found
@patch("api.routes.summary.get_summary")
@patch("api.routes.summary.get_transcript")
def test_get_video_summary_404_no_summary(
    mock_get_transcript, mock_get_summary, client_factory
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_transcript.return_value = TEST_TRANSCRIPT_1
    mock_get_summary.return_value = None

    # ----------------- ACT ------------------
    response = client.get(
        f"/summaries/{TEST_TRANSCRIPT_1.video_id}", headers=TEST_HEADERS
    )
    # ---------------- ASSERT ----------------
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Summary does not exist yet. Please create it first."
    }


# =========================================== POST ===========================================


# Case 201: Summary created
@patch("api.routes.summary.create_summary")
@patch("api.routes.summary.summarize")
@patch("api.routes.summary.get_summary")
@patch("api.routes.summary.get_transcript")
def test_create_video_summary_201(
    mock_get_transcript,
    mock_get_summary,
    mock_summarize,
    mock_create_summary,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_transcript.return_value = TEST_TRANSCRIPT_1
    mock_get_summary.return_value = None
    mock_summarize.return_value = ""
    mock_create_summary.return_value = TEST_SUMMARY_1

    # ----------------- ACT ------------------
    response = client.post(
        f"/summaries/",
        headers=TEST_HEADERS,
        json={"video_id": TEST_TRANSCRIPT_1.video_id},
    )
    expected = {
        "video_id": TEST_TRANSCRIPT_1.video_id,
        "summary_text": TEST_SUMMARY_1.summary_text,
    }

    # ---------------- ASSERT ----------------
    assert mock_get_transcript.call_count == 1
    assert mock_get_summary.call_count == 1
    assert mock_summarize.call_count == 1
    assert mock_create_summary.call_count == 1
    assert response.status_code == 201
    assert response.json() == expected


# Case 400: Invalid YouTube Video ID
def test_create_video_summary_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    # ----------------- ACT ------------------
    response = client.post(
        f"/summaries/", headers=TEST_HEADERS, json={"video_id": "bad_id"}
    )

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid YouTube video ID"}


# Case 401: Unauthorized
def test_create_video_summary_401_unauthorized(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB, auth=False)

    # ----------------- ACT ------------------
    response = client.post(f"/summaries/", json={"video_id": "bad_id"})

    # ---------------- ASSERT ----------------
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


# Case 404: No transcript
@patch("api.routes.summary.get_transcript")
def test_create_video_summary_404_no_transcript(mock_get_transcript, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_transcript.return_value = None
    valid_id = "11111111111"

    # ----------------- ACT ------------------
    response = client.post(
        f"/summaries/",
        headers=TEST_HEADERS,
        json={"video_id": valid_id},
    )

    # ---------------- ASSERT ----------------
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Video is not added yet. Please add the video first."
    }


# Case 409: Summary already exists
@patch("api.routes.summary.create_summary")
@patch("api.routes.summary.summarize")
@patch("api.routes.summary.get_summary")
@patch("api.routes.summary.get_transcript")
def test_create_video_summary_409_summary_exists(
    mock_get_transcript,
    mock_get_summary,
    mock_summarize,
    mock_create_summary,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_transcript.return_value = TEST_TRANSCRIPT_1
    mock_get_summary.return_value = TEST_SUMMARY_1
    mock_summarize.return_value = ""

    # ----------------- ACT ------------------
    response = client.post(
        f"/summaries/",
        headers=TEST_HEADERS,
        json={"video_id": TEST_TRANSCRIPT_1.video_id},
    )

    # ---------------- ASSERT ----------------
    assert mock_get_transcript.call_count == 1
    assert mock_get_summary.call_count == 1
    assert mock_summarize.call_count == 0
    assert mock_create_summary.call_count == 0
    assert response.status_code == 409
    assert response.json() == {"detail": "Summary already exists"}
