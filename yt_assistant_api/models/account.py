from core.db_session import Base

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy


class Account(Base):
    __tablename__ = "account"

    id = Column(String, primary_key=True, index=True)  # Auth0 "sub"

    account_videos = relationship(
        "AccountVideo", back_populates="account", cascade="all, delete-orphan"
    )
    videos = association_proxy("account_videos", "video")
