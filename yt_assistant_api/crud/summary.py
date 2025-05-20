from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Summary
from schemas import SummaryCreate


def create_summary(db: Session, data: SummaryCreate) -> Summary:
    """Create summary"""
    summary = Summary(
        transcript_id=data.transcript_id,
        summary_text=data.summary_text,
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary


def get_summary(db: Session, transcript_id: str) -> Optional[Summary]:
    """Get summary of the transcript"""

    stmt = select(Summary).where(Summary.transcript_id == transcript_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()
