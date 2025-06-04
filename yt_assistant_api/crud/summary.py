from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Summary
from schemas import SummaryCreate


async def create_summary(db: AsyncSession, data: SummaryCreate) -> Summary:
    """Create summary"""
    summary = Summary(
        transcript_id=data.transcript_id,
        summary_text=data.summary_text,
    )
    db.add(summary)
    await db.commit()
    await db.refresh(summary)
    return summary


async def get_summary(db: AsyncSession, transcript_id: str) -> Optional[Summary]:
    """Get summary of the transcript"""

    stmt = select(Summary).where(Summary.transcript_id == transcript_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
