from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.db_session import Base

if TYPE_CHECKING:
    from models import Summary, TranscriptChunk, Video


class Transcript(Base):
    __tablename__ = "transcript"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    video_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("video.id", ondelete="CASCADE"),
        unique=True,  # enforce 1-to-1
        nullable=False,
    )
    transcript_text: Mapped[str] = mapped_column(Text)

    video: Mapped["Video"] = relationship(
        "Video", back_populates="transcript", uselist=False
    )

    summary: Mapped["Summary"] = relationship(
        "Summary",
        back_populates="transcript",
        uselist=False,
        cascade="all, delete-orphan",
    )
    chunks: Mapped[list["TranscriptChunk"]] = relationship(
        "TranscriptChunk", back_populates="transcript", cascade="all, delete-orphan"
    )
