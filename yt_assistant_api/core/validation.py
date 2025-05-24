import re
from fastapi import HTTPException
from .logger import logger

YOUTUBE_VIDEO_ID_REGEX = re.compile(r"^[a-zA-Z0-9_-]{11}$")


def validate_video_id(video_id: str):
    logger.info("Validating video id...")
    if not YOUTUBE_VIDEO_ID_REGEX.match(video_id):
        raise HTTPException(status_code=400, detail="Invalid YouTube video ID")
    return video_id
