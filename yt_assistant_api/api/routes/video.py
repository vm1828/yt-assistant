# TODO: further normalize post endpoint

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger, validate_video_id
from core.exceptions import (
    EXC_400_INVALID_YT_ID,
    EXC_401_NOT_AUTHENTICATED,
    EXC_403_ACCOUNT_NOT_APPROVED,
    EXC_404_NO_VID_OR_TRANSCRIPT,
    EXC_404_USER_VID_NOT_FOUND,
    EXC_409_VID_ALREADY_ADDED_TO_ACC,
    create_responses,
)
from crud.account import get_account_by_id
from crud.video import add_video_to_account, create_video, get_account_video, get_video
from schemas import Auth0Payload
from schemas.video import VideoCreate, VideoRequest, VideoResponse, VideosResponse
from services import fetch_video_title, fetch_video_transcript
from tasks import dispatch_transcript_embedding_task

router = APIRouter()

# ========================================= VIDEOS =========================================

# ------------------------------------------ GET -------------------------------------------


@router.get(
    "/",
    response_model=VideosResponse,
    description="Returns a list of all videos of the authenticated user.",
    responses=create_responses(EXC_401_NOT_AUTHENTICATED, EXC_403_ACCOUNT_NOT_APPROVED),
)
async def get_user_videos(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    account = await get_account_by_id(db, auth0_user.sub, lazy=False)

    videos = account.videos or []
    return VideosResponse(videos=videos)


# ========================================= VIDEO =========================================

# ------------------------------------------ GET ------------------------------------------


@router.get(
    "/{video_id}",
    response_model=VideoResponse,
    description="Returns details of a specific video added to the authenticated user's account.",
    responses=create_responses(
        EXC_400_INVALID_YT_ID,
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_404_USER_VID_NOT_FOUND,
    ),
)
async def get_user_video(
    video_id: str,
    auth0_user=Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    validate_video_id(video_id)

    logger.info("Fetching video from account videos...")
    video = await get_account_video(db, auth0_user.sub, video_id)
    if not video:
        raise EXC_404_USER_VID_NOT_FOUND
    return video


# ------------------------------------------ POST -------------------------------------------


@router.post(
    "/",
    response_model=VideoResponse,
    status_code=status.HTTP_201_CREATED,
    description=(
        "Adds a YouTube video to the authenticated user's account.\n"
        "- If the video is already added by someone else, adds it to the account.\n"
        "- If the video isn't added yet, fetches metadata and transcript, then adds and links to the account.\n"
    ),
    responses=create_responses(
        EXC_400_INVALID_YT_ID,
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_404_NO_VID_OR_TRANSCRIPT,
        EXC_409_VID_ALREADY_ADDED_TO_ACC,
    ),
)
async def add_video(
    payload: VideoRequest,
    auth0_user=Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    video_id = payload.id
    validate_video_id(video_id)

    logger.info(
        "Trying to get video from all videos..."
    )  # Check if video already added by someone else
    video = await get_video(db, video_id, lazy=False)

    if video:
        if any(link.account_id == auth0_user.sub for link in video.account_videos):
            raise EXC_409_VID_ALREADY_ADDED_TO_ACC
        logger.info("Adding existing video to the account...")
        await add_video_to_account(db, auth0_user.sub, video_id)

    else:

        title = await fetch_video_title(video_id)
        transcript_text = await fetch_video_transcript(video_id)

        if not (title and transcript_text):
            raise EXC_404_NO_VID_OR_TRANSCRIPT

        logger.info("Adding new video...")
        data = VideoCreate(id=video_id, title=title, transcript_text=transcript_text)
        video = await create_video(
            db,
            auth0_user.sub,
            data,
        )

        # Trigger async embedding task for new video
        dispatch_transcript_embedding_task(video_id)

    return video
