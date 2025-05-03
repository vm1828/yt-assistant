from unittest.mock import patch, MagicMock
from services import fetch_video_title


@patch("httpx.Client.get")
def test_fetch_video_title_returns_title(mock_get):
    # ---------------- ARRANGE ----------------
    mock_response = MagicMock()
    mock_response.text = """
    <html>
        <head>
            <meta property="og:title" content="Youtube Video Title">
        </head>
    </html>
    """
    mock_get.return_value = mock_response

    # ----------------- ACT ------------------
    title = fetch_video_title("test_video_id")

    # ---------------- ASSERT ----------------
    assert title == "Youtube Video Title"


@patch("httpx.Client.get")
def test_fetch_video_title_no_title(mock_get):
    # ---------------- ARRANGE ----------------
    mock_response = MagicMock()
    mock_response.text = ""
    mock_get.return_value = mock_response

    # ----------------- ACT ------------------
    title = fetch_video_title("test_video_id")

    # ---------------- ASSERT ----------------
    assert title == None
