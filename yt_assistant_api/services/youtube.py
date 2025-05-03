import httpx
from bs4 import BeautifulSoup


def fetch_video_title(video_id: str):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    with httpx.Client() as client:
        response = client.get(video_url)
    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("meta", property="og:title")
    return title_tag["content"] if title_tag else None
