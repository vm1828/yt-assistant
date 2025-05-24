from typing import Optional
import httpx
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

from core import logger

ytt_api = YouTubeTranscriptApi()


async def fetch_video_title(video_id: str):
    logger.info("Fetching video title...")
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(video_url)
    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"] if title_tag else None
    logger.debug(f"Video title: {title}")
    return title


async def fetch_video_transcript(video_id: str) -> Optional[str]:
    logger.info("Fetching video transcript...")
    transcript_text = None
    try:
        transcript = ytt_api.fetch(video_id)
        if transcript:
            transcript_text = " ".join(segment.text for segment in transcript).strip()
        return transcript_text
    except Exception as e:
        logger.error(f"Failed to fetch transcript for {video_id}")
        logger.debug(f"Error: {e}")
        return None
