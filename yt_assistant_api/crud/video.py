from typing import List, Optional
from sqlalchemy.orm import Session

from models import Account, Video, AccountVideo
from schemas import VideoCreate


def get_video(db: Session, video_id: str) -> Optional[Video]:
    """Get video from all videos"""
    return db.query(Video).filter(Video.id == video_id).first()


def get_account_video(db: Session, account: Account, video_id: str) -> Optional[Video]:
    """Get video from account videos"""
    video = next((video for video in account.videos if video.id == video_id), None)
    return video


def create_video(db: Session, account: Account, data: VideoCreate) -> Video:
    """Add new video to the db."""
    video = Video(id=data.id, title=data.title)

    db.add(video)
    db.commit()
    db.refresh(video)

    add_video_to_account(db, account, data.id)

    return video


def add_video_to_account(db: Session, account: Account, video_id: str):
    """Add existing video to user account"""
    account.account_videos.append(
        AccountVideo(account_id=account.id, video_id=video_id)
    )  # Link the video to the account using the proxy (automatic handling of AccountVideo)
    db.add(account)  # Add account with the new relation to session
    db.commit()
    db.refresh(account)
