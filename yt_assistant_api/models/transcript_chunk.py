from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.db_session import Base

if TYPE_CHECKING:
    from models import Embedding, Transcript


class TranscriptChunk(Base):
    __tablename__ = "transcript_chunk"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    transcript_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("transcript.id", ondelete="CASCADE"), nullable=False
    )
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)

    transcript: Mapped["Transcript"] = relationship(
        "Transcript", back_populates="chunks"
    )
    embeddings: Mapped[List["Embedding"]] = relationship(
        "Embedding", back_populates="chunk", cascade="all, delete-orphan"
    )
