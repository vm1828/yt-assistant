from typing import cast
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import get_current_account, get_db, validate_video_id
from crud import (
    get_video,
    get_account_video,
    create_video,
    add_video_to_account,
)
from services import fetch_video_title
from schemas import Auth0Payload, VideoRead, VideoReadList, VideoCreate
from crud.account import get_account_by_id
from models.account import Account


router = APIRouter()


@router.get(
    "/",
    response_model=VideoReadList,
    description="Returns a list of all videos of the authenticated user. ",
)
def get_user_videos(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    account_id = auth0_user.sub
    account = cast(Account, get_account_by_id(db, account_id))

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
def get_user_video(
    video_id: str,
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    validate_video_id(video_id)

    account_id = auth0_user.sub
    account = cast(
        Account, get_account_by_id(db, account_id)
    )  # authorized user always has account

    # Try to get video from account videos
    video = get_account_video(db, account, video_id)
    if not video:

        # Check if video already added by someone else and add it to the user account.
        video = get_video(db, video_id)
        if not video:
            title = fetch_video_title(video_id)
            if not title:
                raise HTTPException(status_code=404, detail="Video not found.")
            data = VideoCreate(id=video_id, title=title)
            video = create_video(db, account, data)
        else:
            add_video_to_account(db, account, video_id)

    return video
