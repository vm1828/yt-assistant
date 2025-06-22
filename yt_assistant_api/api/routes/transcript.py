from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger, validate_video_id
from crud import get_transcript
from schemas import TranscriptResponse

router = APIRouter()


@router.get(
    "/{video_id}",
    response_model=TranscriptResponse,
    description="Returns the transcript of a specific video for the authenticated user.",
    dependencies=[Depends(get_current_account)],
    responses={
        400: {"description": "Invalid YouTube video ID"},
        401: {"description": "Not authenticated"},
        403: {"description": "Account not approved"},
        404: {"description": "No video has been added"},
    },
)
async def get_video_transcript(
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    logger.info("Validating video id...")
    validate_video_id(video_id)

    logger.info("Fetching transcript...")
    transcript = await get_transcript(db, video_id)
    if not transcript:
        raise HTTPException(
            status_code=404,
            detail="No video has been added. Please add a video first.",
        )

    return transcript
