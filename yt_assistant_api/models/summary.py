from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from uuid import uuid4
from core.db_session import Base

if TYPE_CHECKING:
    from models import Transcript


class Summary(Base):
    __tablename__ = "summary"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    transcript_id: Mapped[str] = mapped_column(
        Uuid,
        ForeignKey("transcript.id", ondelete="CASCADE"),
        unique=True,  # MVP, TODO - user custom summaries, different types of summary etc.
        nullable=False,
    )
    summary_text: Mapped[str] = mapped_column(Text)

    transcript: Mapped["Transcript"] = relationship(
        "Transcript", back_populates="summary", uselist=False
    )
