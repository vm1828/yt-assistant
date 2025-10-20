from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.db_session import Base

if TYPE_CHECKING:
    from models import Message


class Conversation(Base):
    # TODO make 1-to-1 with AccountVideo (create account_video id, use it as FK, on delete remove orphaned entries).

    __tablename__ = "conversation"
    __table_args__ = (
        UniqueConstraint(
            "account_id", "video_id", name="uq_conversation_account_video"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    account_id: Mapped[str] = mapped_column(
        String, ForeignKey("account.id"), nullable=False
    )
    video_id: Mapped[str] = mapped_column(
        String, ForeignKey("video.id"), nullable=False
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )
