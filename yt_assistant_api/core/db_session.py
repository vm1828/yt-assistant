from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

Base = declarative_base()

# ---------------- SYNC ENGINE ----------------
engine = create_engine(settings.POSTGRES_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_sync():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- ASYNC ENGINE ----------------
ASYNC_POSTGRES_URL = settings.POSTGRES_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)
async_engine = create_async_engine(ASYNC_POSTGRES_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db_async():
    async with AsyncSessionLocal() as session:
        yield session
