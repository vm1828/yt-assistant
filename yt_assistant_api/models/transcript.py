from sqlalchemy import String, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from core.db_session import Base


class Transcript(Base):
    __tablename__ = "transcript"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid4)
    video_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("video.id", ondelete="CASCADE"),
        unique=True,  # enforce 1-to-1
    )
    text: Mapped[str] = mapped_column(Text)

    video = relationship("Video", back_populates="transcript", uselist=False)
