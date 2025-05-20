from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import (
    get_current_account,
    get_db_sync,
    validate_video_id,
    logger,
)
from crud import get_transcript
from schemas import TranscriptResponse


router = APIRouter()


@router.get(
    "/{video_id}",
    response_model=TranscriptResponse,
    description="Returns transcript of a specific video for the authenticated user.",
    dependencies=[Depends(get_current_account)],
)
def get_video_transcript(
    video_id: str,
    db: Session = Depends(get_db_sync),
):
    logger.info("Validating video id...")
    validate_video_id(video_id)

    logger.info("Fetching transcript...")

    transcript = get_transcript(db, video_id)
    if not transcript:
        raise HTTPException(
            status_code=404,
            detail="Video is not added yet. Please add the video first.",
        )

    return transcript
