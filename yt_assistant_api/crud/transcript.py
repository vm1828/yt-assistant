from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Transcript


async def get_transcript(db: AsyncSession, video_id: str) -> Optional[Transcript]:
    """Get transcript of the video"""
    stmt = select(Transcript).where(Transcript.video_id == video_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
