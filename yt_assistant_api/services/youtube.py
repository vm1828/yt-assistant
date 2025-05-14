from typing import Optional
import httpx
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi


async def fetch_video_title(video_id: str):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(video_url)
    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("meta", property="og:title")
    return title_tag["content"] if title_tag else None


async def fetch_video_transcript(video_id: str) -> Optional[str]:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return (
        " ".join(segment["text"] for segment in transcript).strip()
        if transcript
        else None
    )
