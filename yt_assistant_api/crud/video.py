from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models import Video, AccountVideo, Transcript
from schemas import VideoCreate


async def get_video(db: AsyncSession, video_id: str, lazy=True) -> Optional[Video]:
    """Get video from all videos"""
    stmt = select(Video).where(Video.id == video_id)

    if not lazy:
        stmt = stmt.options(selectinload(Video.account_videos))

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_account_video(
    db: AsyncSession, account_id: str, video_id: str
) -> Optional[Video]:
    """Get video from the database related to the account."""
    stmt = (
        select(Video)
        .join(Video.account_videos)
        .where(AccountVideo.account_id == account_id)
        .where(Video.id == video_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_video(
    db: AsyncSession,
    account_id: str,
    data: VideoCreate,
) -> Video:
    """Add a new video, its transcript, and link it to the user."""

    video = Video(id=data.id, title=data.title)
    db.add(video)

    transcript = Transcript(video_id=data.id, transcript_text=data.transcript_text)
    db.add(transcript)

    await add_video_to_account(db, account_id, data.id)  # will also commit

    return video


async def add_video_to_account(db: AsyncSession, account_id: str, video_id: str):
    """Add existing video to user account."""
    link = AccountVideo(account_id=account_id, video_id=video_id)
    db.add(link)
    await db.commit()
