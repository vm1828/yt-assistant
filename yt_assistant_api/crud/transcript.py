from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Transcript


def get_transcript(db: Session, video_id: str) -> Optional[Transcript]:
    """Get transcript of the video"""
    stmt = select(Transcript).where(Transcript.video_id == video_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()
