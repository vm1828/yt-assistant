from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger, validate_video_id
from core.exceptions import (
    EXC_400_INVALID_YT_ID,
    EXC_401_NOT_AUTHENTICATED,
    EXC_403_ACCOUNT_NOT_APPROVED,
    EXC_404_SUMM_NOT_FOUND,
    EXC_404_VID_NOT_ADDED,
    EXC_409_SUMM_ALREADY_EXISTS,
    create_responses,
)
from crud import create_summary, get_summary, get_transcript
from schemas import SummaryCreate, SummaryRequest, SummaryResponse
from services import summarize

router = APIRouter()

# ------------------------------------------ GET -------------------------------------------


@router.get(
    "/{video_id}",
    response_model=SummaryResponse,
    description="Returns the summary of a video transcript for the authenticated user.",
    dependencies=[Depends(get_current_account)],
    responses=create_responses(
        EXC_400_INVALID_YT_ID,
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_404_SUMM_NOT_FOUND,
    ),
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
        raise EXC_404_VID_NOT_ADDED

    summary = await get_summary(db, transcript.id)
    if not summary:
        raise EXC_404_SUMM_NOT_FOUND

    return SummaryResponse(video_id=video_id, summary_text=summary.summary_text)


# ------------------------------------------ POST -------------------------------------------


@router.post(
    "/",
    response_model=SummaryResponse,
    status_code=status.HTTP_201_CREATED,
    description="Creates a summary of a video transcript for the authenticated user.",
    dependencies=[Depends(get_current_account)],
    responses=create_responses(
        EXC_400_INVALID_YT_ID,
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_404_VID_NOT_ADDED,
        EXC_409_SUMM_ALREADY_EXISTS,
    ),
)
async def create_video_summary(
    payload: SummaryRequest,
    db: AsyncSession = Depends(get_db),
):
    video_id = payload.video_id
    validate_video_id(video_id)

    transcript = await get_transcript(db, video_id)
    if not transcript:
        raise EXC_404_VID_NOT_ADDED

    if await get_summary(db, transcript.id):
        raise EXC_409_SUMM_ALREADY_EXISTS

    summary_text = summarize(transcript.transcript_text)
    data = SummaryCreate(summary_text=summary_text, transcript_id=transcript.id)
    summary = await create_summary(db, data)

    return SummaryResponse(video_id=video_id, summary_text=summary.summary_text)
