from datetime import datetime

from models import (
    Account,
    AccountVideo,
    Conversation,
    Message,
    Summary,
    Transcript,
    Video,
)

TEST_HEADERS = {"Authorization": "Bearer test_token"}

TEST_USER_1_SUB = "auth0|12345"
TEST_USER_2_SUB = "google-oauth2|114326681879294310515"

TEST_VIDEO_1 = Video(id="dCLhUialKPQ", title="React JS 19 Full Course 2025")
TEST_TRANSCRIPT_1 = Transcript(
    id="b0c43684-4978-43b4-9488-6b8a63f2a764",
    video_id=TEST_VIDEO_1.id,
    created_at=datetime(2025, 1, 1, 0, 0, 0),
    transcript_text="React JS 19 Full Course 2025 transcript.",
)
TEST_SUMMARY_1 = Summary(
    id="c044d534-8475-23lb-1299-2k4363f2s994",
    created_at=datetime(2025, 1, 1, 0, 5, 0),
    transcript_id=TEST_TRANSCRIPT_1.id,
    summary_text="React JS 19 Full Course 2025 summary.",
)
TEST_CONV_1_EMPTY = Conversation(
    id="b3e1f5a2-9c1d-4f2b-8e5d-7a4c2b1f9d6a",
    account_id=TEST_USER_1_SUB,
    video_id=TEST_VIDEO_1.id,
    created_at=datetime(2025, 1, 1, 0, 10, 0),
    messages=[],
)
TEST_CONV_1_MESSAGE_1 = Message(
    id="a1c2d3e4-5f67-4890-8abc-1def23456789",
    conversation_id=TEST_CONV_1_EMPTY.id,
    created_at=datetime(2025, 1, 1, 0, 10, 5),
    user_message="Hello, explain React hooks.",
    ai_response="Sure! React hooks let you use state and effects in functional components.",
)
TEST_CONV_1_MESSAGE_2 = Message(
    id="b2d3f4a5-6c78-4b90-9def-2abc34567890",
    conversation_id=TEST_CONV_1_EMPTY.id,
    created_at=datetime(2025, 1, 1, 0, 10, 10),
    user_message="What about useEffect?",
    ai_response="useEffect lets you run side effects in functional components...",
)
TEST_CONV_1 = Conversation(
    id=TEST_CONV_1_EMPTY.id,
    account_id=TEST_USER_1_SUB,
    video_id=TEST_VIDEO_1.id,
    created_at=datetime(2025, 1, 1, 0, 10, 0),
    messages=[TEST_CONV_1_MESSAGE_1, TEST_CONV_1_MESSAGE_2],
)
TEST_VIDEO_2 = Video(id="1R5u3xQUUqI", title="Hamster Escapes from the Prison Maze")
TEST_VIDEO_3 = Video(id="eMlx5fFNoYc", title="Attention in transformers, step-by-step")

TEST_ACCOUNT_1_VIDEO_1 = AccountVideo(
    account_id=TEST_USER_1_SUB,
    video_id=TEST_VIDEO_1.id,
    created_at=datetime.fromisoformat("2022-02-21T14:15:39.795572"),
)
TEST_ACCOUNT_1_VIDEO_2 = AccountVideo(
    account_id=TEST_USER_1_SUB,
    video_id=TEST_VIDEO_2.id,
    created_at=datetime.fromisoformat("2022-02-21T15:15:39.795572"),
)
TEST_ACCOUNT_2_VIDEO_1 = AccountVideo(
    account_id=TEST_USER_2_SUB,
    video_id=TEST_VIDEO_3.id,
    created_at=datetime.fromisoformat("2025-05-01T18:15:39.795572"),
)
TEST_ACCOUNT_2_VIDEO_2 = AccountVideo(
    account_id=TEST_USER_2_SUB,
    video_id=TEST_VIDEO_2.id,
    created_at=datetime.fromisoformat("2025-05-01T19:15:39.795572"),
)

TEST_ACCOUNT_1 = Account(
    id=TEST_USER_1_SUB,
    account_videos=[AccountVideo(video=TEST_VIDEO_1), AccountVideo(video=TEST_VIDEO_2)],
)
TEST_ACCOUNT_2 = Account(
    id=TEST_USER_2_SUB, account_videos=[TEST_ACCOUNT_2_VIDEO_1, TEST_ACCOUNT_2_VIDEO_2]
)
