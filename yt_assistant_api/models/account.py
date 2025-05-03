from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.ext.associationproxy import association_proxy

from core.db_session import Base
from models.video import Video
from models.accout_video import AccountVideo


class Account(Base):
    __tablename__ = "account"

    id = Column(String, primary_key=True, index=True)  # Auth0 "sub"

    account_videos: Mapped[List[AccountVideo]] = relationship(
        "AccountVideo", back_populates="account", cascade="all, delete-orphan"
    )
    videos: Mapped[List[Video]] = association_proxy("account_videos", "video")
