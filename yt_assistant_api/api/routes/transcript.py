from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger, validate_video_id
from core.constants import (
    RESP_400_INVALID_YT_ID,
    RESP_401_NOT_AUTHENTICATED,
    RESP_403_ACCOUNT_NOT_APPROVED,
)
from crud import get_transcript
from schemas import TranscriptResponse

router = APIRouter()


@router.get(
    "/{video_id}",
    response_model=TranscriptResponse,
    description="Returns the transcript of a specific video for the authenticated user.",
    dependencies=[Depends(get_current_account)],
    responses={
        400: RESP_400_INVALID_YT_ID,
        401: RESP_401_NOT_AUTHENTICATED,
        403: RESP_403_ACCOUNT_NOT_APPROVED,
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
