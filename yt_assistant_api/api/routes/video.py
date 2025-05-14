from typing import cast
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import (
    get_current_account,
    get_db_sync,
    get_db_async,
    validate_video_id,
    logger,
)
from crud import (
    get_video,
    get_account_video,
    create_video,
    add_video_to_account,
)
from services import fetch_video_title, fetch_video_transcript
from schemas import Auth0Payload, VideoRead, VideoReadList, VideoCreate
from crud.account import get_account_by_id_sync, get_account_by_id_async
from models.account import Account


router = APIRouter()


@router.get(
    "/",
    response_model=VideoReadList,
    description="Returns a list of all videos of the authenticated user. ",
)
def get_user_videos(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: Session = Depends(get_db_sync),
):
    logger.info("Fetching user account...")
    account_id = auth0_user.sub
    account = cast(Account, get_account_by_id_sync(db, account_id))

    if not account.videos:
        raise HTTPException(status_code=404, detail="No videos found for this user.")

    return {"videos": account.videos}


@router.get(
    "/{video_id}",
    response_model=VideoRead,
    description="""Returns details of a specific video for the authenticated user.
    If the video doesn't exist, it will attempt to fetch the title from YouTube and create a new video entry.
    If the title cannot be fetched, an error will be raised.""",
)
async def get_user_video(
    video_id: str,
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: Session = Depends(get_db_async),
):
    logger.info("Validating video id...")
    validate_video_id(video_id)

    logger.info("Fetching user account...")
    account_id = auth0_user.sub
    account = cast(
        Account, await get_account_by_id_async(db, account_id)
    )  # authorized user always has account

    logger.info("Trying to get video from account videos...")
    video = await get_account_video(db, account, video_id)
    if not video:

        logger.info(
            "Trying to get video from all videos..."
        )  # Check if video already added by someone else and add it to the user account.
        video = await get_video(db, video_id)

        if not video:

            logger.info("Fetching video title...")
            title = await fetch_video_title(video_id)
            transcript = await fetch_video_transcript(video_id)

            if not (title and transcript):
                raise HTTPException(
                    status_code=404,
                    detail="Video not found or without a transcript.",
                )

            logger.info("Adding new video...")
            data = VideoCreate(id=video_id, title=title)
            video = await create_video(db, account, data, transcript)

        else:

            logger.info("Adding existing video to the account...")
            await add_video_to_account(db, account, video_id)

    return video
