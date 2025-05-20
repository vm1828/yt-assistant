from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from uuid import uuid4
from core.db_session import Base

if TYPE_CHECKING:
    from models import Video, Summary


class Transcript(Base):
    __tablename__ = "transcript"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
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
