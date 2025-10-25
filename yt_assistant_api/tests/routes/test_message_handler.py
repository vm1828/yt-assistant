import uuid
from unittest.mock import patch

from core.exceptions import EXC_401_NOT_AUTHENTICATED, EXC_404_CONV_NOT_ADDED
from tests.data import (
    TEST_CONV_1,
    TEST_CONV_1_EMPTY,
    TEST_CONV_1_MESSAGE_1,
    TEST_CONV_1_MESSAGE_2,
    TEST_HEADERS,
    TEST_USER_1_SUB,
)

# =========================================== POST ===========================================


# Case 201: Message created successfully
@patch("api.routes.message.create_message")
@patch("api.routes.message.get_ai_response")
@patch("api.routes.message.get_conversation_by_id")
def test_post_message_201(
    mock_get_conversation_by_id,
    mock_get_ai_response,
    mock_create_message,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_conversation_by_id.return_value = TEST_CONV_1_EMPTY
    mock_get_ai_response.return_value = TEST_CONV_1_MESSAGE_1.ai_response
    mock_create_message.return_value = TEST_CONV_1_MESSAGE_1
    payload = {
        "conversation_id": TEST_CONV_1_MESSAGE_1.conversation_id,
        "user_message": TEST_CONV_1_MESSAGE_1.user_message,
    }

    # ----------------- ACT ------------------
    response = client.post("/messages/", headers=TEST_HEADERS, json=payload)
    expected = {
        "id": TEST_CONV_1_MESSAGE_1.id,
        "conversation_id": TEST_CONV_1_MESSAGE_1.conversation_id,
        "user_message": TEST_CONV_1_MESSAGE_1.user_message,
        "ai_response": TEST_CONV_1_MESSAGE_1.ai_response,
    }

    # ---------------- ASSERT ----------------
    assert mock_get_conversation_by_id.call_count == 1
    assert mock_get_ai_response.call_count == 1
    assert mock_create_message.call_count == 1
    assert response.status_code == 201
    assert response.json() == expected


# Case 401: Unauthorized
def test_post_message_401_unauthorized(client_factory):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB, auth=False)

    # ----------------- ACT ------------------
    response = client.post(
        "/messages/",
        json={
            "conversation_id": TEST_CONV_1_MESSAGE_1.conversation_id,
            "user_message": TEST_CONV_1_MESSAGE_1.user_message,
        },
    )

    # ---------------- ASSERT ----------------
    assert response.status_code == 401
    assert response.json()["detail"] == EXC_401_NOT_AUTHENTICATED.detail


# Case 404: Conversation not found
@patch("api.routes.message.get_conversation_by_id")
def test_post_message_404_conversation_not_found(
    mock_get_conversation_by_id,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    mock_get_conversation_by_id.return_value = None

    # ----------------- ACT ------------------
    response = client.post(
        "/messages/",
        headers=TEST_HEADERS,
        json={"conversation_id": str(uuid.uuid4()), "user_message": "Hi"},
    )

    # ---------------- ASSERT ----------------
    assert response.status_code == 404
    assert response.json()["detail"] == EXC_404_CONV_NOT_ADDED.detail


# Case sanity: AI response is called with full history context
@patch("api.routes.message.create_message")
@patch("api.routes.message.get_ai_response")
@patch("api.routes.message.get_conversation_by_id")
def test_post_message_context_aware_prompt(
    mock_get_conversation_by_id,
    mock_get_ai_response,
    mock_create_message,
    client_factory,
):
    # ---------------- ARRANGE ----------------
    client = client_factory(TEST_USER_1_SUB)
    conversation = TEST_CONV_1
    conversation.messages = [
        TEST_CONV_1_MESSAGE_1,  # existing messages in conversation
    ]
    mock_get_conversation_by_id.return_value = conversation
    mock_get_ai_response.return_value = TEST_CONV_1_MESSAGE_2.ai_response
    mock_create_message.return_value = TEST_CONV_1_MESSAGE_2

    payload = {
        "conversation_id": conversation.id,
        "user_message": TEST_CONV_1_MESSAGE_2.user_message,
    }

    # ----------------- ACT ------------------
    client.post("/messages/", headers=TEST_HEADERS, json=payload)

    # ---------------- ASSERT ----------------
    assert mock_get_conversation_by_id.call_count == 1
    assert mock_get_ai_response.call_count == 1
    prompt_arg = mock_get_ai_response.call_args[0][0]
    assert "User:" in prompt_arg
    assert "Assistant:" in prompt_arg
    assert TEST_CONV_1_MESSAGE_1.user_message in prompt_arg
    assert TEST_CONV_1_MESSAGE_1.ai_response in prompt_arg
    assert TEST_CONV_1_MESSAGE_2.user_message in prompt_arg
