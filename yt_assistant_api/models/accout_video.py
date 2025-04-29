from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func
from core.db_session import Base


class AccountVideo(Base):
    __tablename__ = "account_video"

    account_id = Column(String, ForeignKey("account.id"), primary_key=True)
    video_id = Column(String, ForeignKey("video.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    account = relationship("Account", back_populates="account_videos")
    video = relationship("Video", back_populates="account_videos")
