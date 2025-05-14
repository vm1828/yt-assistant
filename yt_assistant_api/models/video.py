from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.db_session import Base

if TYPE_CHECKING:
    from models import AccountVideo, Transcript


class Video(Base):
    __tablename__ = "video"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True
    )  # (e.g., "dQw4w9WgXcQ")
    title: Mapped[str] = mapped_column(String, nullable=False)

    account_videos: Mapped[List["AccountVideo"]] = relationship(
        "AccountVideo", back_populates="video"
    )
    transcript: Mapped["Transcript"] = relationship(
        "Transcript",
        back_populates="video",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )
