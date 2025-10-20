import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Conversation
from schemas import ConversationCreate

logger = logging.getLogger(__name__)


async def get_conversation_by_user_and_video(
    db: AsyncSession, account_id: str, video_id: str, lazy: bool = True
) -> Conversation | None:
    stmt = select(Conversation).where(
        Conversation.account_id == account_id, Conversation.video_id == video_id
    )

    if not lazy:
        stmt = stmt.options(selectinload(Conversation.messages))

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_conversation(
    db: AsyncSession, data: ConversationCreate
) -> Conversation:
    """Create conversation"""
    conversation = Conversation(
        account_id=data.account_id,
        video_id=data.video_id,
    )
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation
