from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.ext.associationproxy import association_proxy

from core.db_session import Base

if TYPE_CHECKING:
    from models import AccountVideo, Video


class Account(Base):
    __tablename__ = "account"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)  # Auth0 "sub"

    account_videos: Mapped[List["AccountVideo"]] = relationship(
        "AccountVideo", back_populates="account", cascade="all, delete-orphan"
    )
    videos: List["Video"] = association_proxy("account_videos", "video")
