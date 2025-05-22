from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import (
    get_current_account,
    get_db_sync,
    validate_video_id,
    logger,
)
from api import router
from crud import get_transcript
from schemas import SummaryResponse, SummaryCreate
from services import summarize
from crud import get_summary, create_summary

router = APIRouter()


@router.get(
    "/{video_id}",
    response_model=SummaryResponse,
    description="Returns summary of a video transcript for the authenticated user.",
    dependencies=[Depends(get_current_account)],
)
def get_video_summary(
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

    logger.info("Trying to fetch summary...")
    summary = get_summary(db, transcript.id)

    if not summary:
        logger.info("Creating summary...")
        summary_text = summarize(transcript.transcript_text)

        logger.info("Saving summary to db...")
        data = SummaryCreate(summary_text=summary_text, transcript_id=transcript.id)
        summary = create_summary(db, data)

    return SummaryResponse(video_id=video_id, summary_text=summary.summary_text)
