from sqlalchemy.ext.asyncio import AsyncSession

from models import Message
from schemas import MessageCreate


async def create_message(db: AsyncSession, data: MessageCreate) -> Message:
    """Create message"""
    message = Message(**data.model_dump())
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message
