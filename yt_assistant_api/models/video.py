from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from core.db_session import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(String, primary_key=True, index=True)  # (e.g., "dQw4w9WgXcQ")
    title = Column(String)

    account_videos = relationship("AccountVideo", back_populates="video")
