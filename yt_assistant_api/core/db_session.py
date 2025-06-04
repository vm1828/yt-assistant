from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

Base = declarative_base()

# ---------------- SYNC ENGINE ----------------
engine = create_engine(settings.POSTGRES_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
