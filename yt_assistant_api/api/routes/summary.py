from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import (
    get_current_account,
    get_db,
    validate_video_id,
    logger,
)
from api import router
from crud import get_transcript
from schemas.summary import *
from services import summarize
from crud import get_summary, create_summary

router = APIRouter()

# ------------------------------------------ GET -------------------------------------------


@router.get(
    "/{video_id}",
    response_model=SummaryResponse,
    description="Get existing summary of a video transcript for the authenticated user.",
    dependencies=[Depends(get_current_account)],
    responses={
        400: {"description": "Invalid YouTube video ID"},
        401: {"description": "Not authenticated"},
        404: {"description": "Summary does not exist yet"},
    },
)
async def get_video_summary(
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    validate_video_id(video_id)

    logger.info("Fetching transcript...")
    transcript = await get_transcript(
        db, video_id
    )  # TODO denormalize Summary by adding `video_id` for querying it directly
    if not transcript:
        raise HTTPException(404, "Video is not added yet. Please add the video first.")

    summary = await get_summary(db, transcript.id)
    if not summary:
        raise HTTPException(404, "Summary does not exist yet. Please create it first.")

    return SummaryResponse(video_id=video_id, summary_text=summary.summary_text)


# ------------------------------------------ POST -------------------------------------------


@router.post(
    "/",
    response_model=SummaryResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a summary of a video transcript for the authenticated user.",
    dependencies=[Depends(get_current_account)],
    responses={
        400: {"description": "Invalid YouTube video ID"},
        401: {"description": "Not authenticated"},
        404: {"description": "Video is not added yet"},
        409: {"description": "Summary already exists"},
    },
)
async def create_video_summary(
    payload: SummaryRequest,
    db: AsyncSession = Depends(get_db),
):
    video_id = payload.video_id
    validate_video_id(video_id)

    transcript = await get_transcript(db, video_id)
    if not transcript:
        raise HTTPException(404, "Video is not added yet. Please add the video first.")

    if await get_summary(db, transcript.id):
        raise HTTPException(409, "Summary already exists")

    summary_text = summarize(transcript.transcript_text)
    data = SummaryCreate(summary_text=summary_text, transcript_id=transcript.id)
    summary = await create_summary(db, data)

    return SummaryResponse(video_id=video_id, summary_text=summary.summary_text)
