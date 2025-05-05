from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.db_session import Base

if TYPE_CHECKING:
    from models import AccountVideo


class Video(Base):
    __tablename__ = "video"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True
    )  # (e.g., "dQw4w9WgXcQ")
    title: Mapped[str] = mapped_column(String)

    account_videos: Mapped[List["AccountVideo"]] = relationship(
        "AccountVideo", back_populates="video"
    )
