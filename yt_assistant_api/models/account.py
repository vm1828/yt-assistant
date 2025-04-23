from sqlalchemy import Column, String

# from sqlalchemy.orm import relationship
from core.db_session import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(String, primary_key=True, index=True)  # Auth0 "sub"

    # videos = relationship("Video", back_populates="account")
    # qas = relationship("QA", back_populates="account")
