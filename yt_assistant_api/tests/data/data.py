from datetime import datetime
from models import Account, Video, AccountVideo, Transcript, Summary

TEST_HEADERS = {"Authorization": "Bearer test_token"}

TEST_USER_1_SUB = "auth0|12345"
TEST_USER_2_SUB = "google-oauth2|114326681879294310515"

TEST_VIDEO_1 = Video(id="dCLhUialKPQ", title="React JS 19 Full Course 2025")
TEST_TRANSCRIPT_1 = Transcript(
    id="b0c43684-4978-43b4-9488-6b8a63f2a764",
    video_id="dCLhUialKPQ",
    created_at=datetime(2025, 1, 1, 0, 0, 0),
    transcript_text="React JS 19 Full Course 2025 transcript.",
)
TEST_SUMMARY_1 = Summary(
    id="c044d534-8475-23lb-1299-2k4363f2s994",
    created_at=datetime(2025, 1, 1, 0, 5, 0),
    transcript_id="b0c43684-4978-43b4-9488-6b8a63f2a764",
    summary_text="React JS 19 Full Course 2025 summary.",
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
