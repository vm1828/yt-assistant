from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.db_session import Base

if TYPE_CHECKING:
    from models import TranscriptChunk


class Embedding(Base):
    __tablename__ = "embedding"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    transcript_chunk_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("transcript_chunk.id", ondelete="CASCADE"), nullable=False
    )
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)
    chunk: Mapped["TranscriptChunk"] = relationship(
        "TranscriptChunk", back_populates="embeddings"
    )
