# TODO: further normalize post endpoint

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import (
    get_current_account,
    get_db_async,
    validate_video_id,
    logger,
)
from schemas import Auth0Payload
from schemas.video import *
from crud.account import get_account_by_id_async
from crud.video import *
from services import fetch_video_title, fetch_video_transcript


router = APIRouter()


# ========================================= VIDEOS =========================================

# ------------------------------------------ GET -------------------------------------------


@router.get(
    "/",
    response_model=VideosResponse,
    description="Returns a list of all videos of the authenticated user. ",
)
async def get_user_videos(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: AsyncSession = Depends(get_db_async),
):
    account = await get_account_by_id_async(db, auth0_user.sub, lazy=False)

    videos = account.videos or []
    return VideosResponse(videos=videos)


# ========================================= VIDEO =========================================

# ------------------------------------------ GET ------------------------------------------


@router.get(
    "/{video_id}",
    response_model=VideoResponse,
    description="Returns details of a specific video added to the account of the authenticated user.",
    responses={
        400: {"description": "Invalid YouTube video ID"},
        404: {"description": "Video not found for this user"},
    },
)
async def get_user_video(
    video_id: str,
    auth0_user=Depends(get_current_account),
    db: AsyncSession = Depends(get_db_async),
):
    validate_video_id(video_id)

    logger.info("Fetching video from account videos...")
    video = await get_account_video(db, auth0_user.sub, video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found for this user",
        )
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
    responses={
        400: {"description": "Invalid YouTube video ID"},
        404: {"description": "Video not found or failed to fetch a transcript"},
        409: {"description": "Video already added to the account"},
    },
)
async def add_video(
    payload: VideoRequest,
    auth0_user=Depends(get_current_account),
    db: AsyncSession = Depends(get_db_async),
):
    video_id = payload.id
    validate_video_id(video_id)

    logger.info(
        "Trying to get video from all videos..."
    )  # Check if video already added by someone else
    video = await get_video(db, video_id, lazy=False)

    if video:
        if any(link.account_id == auth0_user.sub for link in video.account_videos):
            raise HTTPException(
                status_code=409, detail="Video already added to the account"
            )
        logger.info("Adding existing video to the account...")
        await add_video_to_account(db, auth0_user.sub, video_id)

    else:

        title = await fetch_video_title(video_id)
        transcript_text = await fetch_video_transcript(video_id)

        if not (title and transcript_text):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found or failed to fetch a transcript",
            )

        logger.info("Adding new video...")
        data = VideoCreate(id=video_id, title=title, transcript_text=transcript_text)
        video = await create_video(
            db,
            auth0_user.sub,
            data,
        )

    return video
