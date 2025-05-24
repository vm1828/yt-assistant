from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from core.db_session import Base

if TYPE_CHECKING:
    from models import Account, Video


class AccountVideo(Base):
    __tablename__ = "account_video"

    account_id: Mapped[str] = mapped_column(
        String, ForeignKey("account.id"), primary_key=True
    )
    video_id: Mapped[str] = mapped_column(
        String, ForeignKey("video.id"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    account: Mapped["Account"] = relationship(
        "Account", back_populates="account_videos"
    )
    video: Mapped["Video"] = relationship("Video", back_populates="account_videos")
