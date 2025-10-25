from unittest.mock import patch

from core.exceptions import (
    EXC_400_INVALID_YT_ID,
    EXC_401_NOT_AUTHENTICATED,
    EXC_404_CONV_NOT_FOUND,
    EXC_409_CONV_ALREADY_EXISTS,
)
from schemas import ConversationResponse
from tests.data import TEST_CONV_1, TEST_CONV_1_EMPTY, TEST_USER_1_SUB, TEST_VIDEO_1

# =========================================== GET ===========================================


# Case 200: Conversation exists and contains messages
@patch("api.routes.conversation.get_conversation_by_user_and_video")
def test_get_conversation_200(mock_get_conv, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_conv.return_value = TEST_CONV_1
    test_video_id = TEST_VIDEO_1.id

    # ----------------- ACT ------------------
    response = client.get(f"/conversations/{test_video_id}")
    expected: ConversationResponse = {
        "id": TEST_CONV_1.id,
        "video_id": test_video_id,
        "messages": [
            {
                "user_message": TEST_CONV_1.messages[0].user_message,
                "ai_response": TEST_CONV_1.messages[0].ai_response,
            },
            {
                "user_message": TEST_CONV_1.messages[1].user_message,
                "ai_response": TEST_CONV_1.messages[1].ai_response,
            },
        ],
    }

    # ---------------- ASSERT ----------------
    assert response.status_code == 200
    assert response.json() == expected


# Case 400: Invalid YouTube Video ID
def test_get_conversation_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    invalid_video_id = "bad_id"

    # ----------------- ACT ------------------
    response = client.get(f"/conversations/{invalid_video_id}")

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json()["detail"] == EXC_400_INVALID_YT_ID.detail


# Case 401: Unauthorized
def test_get_conversation_401_unauthorized(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB, auth=False)

    # ----------------- ACT ------------------
    response = client.get(f"/conversations/{TEST_VIDEO_1.id}")

    # ---------------- ASSERT ----------------
    assert response.status_code == 401
    assert response.json()["detail"] == EXC_401_NOT_AUTHENTICATED.detail


# Case 401: Conversation not found
@patch("api.routes.conversation.get_conversation_by_user_and_video")
def test_get_conversation_404_not_found(mock_get_conv, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_conv.return_value = None

    # ----------------- ACT ------------------
    response = client.get(f"/conversations/{TEST_VIDEO_1.id}")

    # ---------------- ASSERT ----------------
    assert response.status_code == 404
    assert response.json()["detail"] == EXC_404_CONV_NOT_FOUND.detail


# =========================================== POST ===========================================


# Case 201: Conversation created
@patch("api.routes.conversation.create_conversation")
@patch("api.routes.conversation.get_conversation_by_user_and_video")
def test_post_conversation_201(mock_get_conv, mock_create_conv, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    test_video_id = TEST_VIDEO_1.id

    mock_get_conv.return_value = None
    mock_create_conv.return_value = TEST_CONV_1_EMPTY

    # ----------------- ACT ------------------
    response = client.post("/conversations/", json={"video_id": test_video_id})
    expected: ConversationResponse = {
        "id": TEST_CONV_1.id,
        "video_id": test_video_id,
        "messages": [],
    }

    # ---------------- ASSERT ----------------
    assert mock_get_conv.call_count == 1
    assert mock_create_conv.call_count == 1
    assert response.status_code == 201
    assert response.json() == expected


# Case 400: Invalid YouTube Video ID
def test_post_conversation_400_invalid_video_id(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)

    # ----------------- ACT ------------------
    response = client.post("/conversations/", json={"video_id": "bad_id"})

    # ---------------- ASSERT ----------------
    assert response.status_code == 400
    assert response.json()["detail"] == EXC_400_INVALID_YT_ID.detail


# Case 401: Unauthorized
def test_get_conversation_401_unauthorized(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB, auth=False)

    # ----------------- ACT ------------------
    response = client.post("/conversations/", json={"video_id": TEST_VIDEO_1.id})

    # ---------------- ASSERT ----------------
    assert response.status_code == 401
    assert response.json()["detail"] == EXC_401_NOT_AUTHENTICATED.detail


# Case 409: Conversation already exists
@patch("api.routes.conversation.get_conversation_by_user_and_video")
def test_post_conversation_409_already_exists(mock_get_conv, client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_conv.return_value = TEST_CONV_1_EMPTY

    # ----------------- ACT ------------------
    response = client.post("/conversations/", json={"video_id": TEST_VIDEO_1.id})

    # ---------------- ASSERT ----------------
    assert mock_get_conv.call_count == 1
    assert response.status_code == 409
    assert response.json()["detail"] == EXC_409_CONV_ALREADY_EXISTS.detail
