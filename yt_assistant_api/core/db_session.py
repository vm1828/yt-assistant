from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings


engine = create_engine(settings.POSTGRES_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # base class for model definitions


# Dependency to get the DB session in route handlers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
