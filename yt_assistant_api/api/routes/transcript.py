from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger, validate_video_id
from core.exceptions import (
    EXC_400_INVALID_YT_ID,
    EXC_401_NOT_AUTHENTICATED,
    EXC_403_ACCOUNT_NOT_APPROVED,
    EXC_404_VID_NOT_ADDED,
    create_responses,
)
from crud import get_transcript
from schemas import TranscriptResponse

router = APIRouter()


@router.get(
    "/{video_id}",
    response_model=TranscriptResponse,
    description="Returns the transcript of a specific video for the authenticated user.",
    dependencies=[Depends(get_current_account)],
    responses=create_responses(
        EXC_400_INVALID_YT_ID,
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_404_VID_NOT_ADDED,
    ),
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
        raise EXC_404_VID_NOT_ADDED

    return transcript
