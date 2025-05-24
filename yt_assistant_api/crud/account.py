from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core import logger
from models import Account, AccountVideo
from schemas import AccountCreate


async def create_account(db: AsyncSession, data: AccountCreate):
    account = Account(id=data.id)
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


async def get_account_by_id_async(db: AsyncSession, account_id: str, lazy: bool = True):
    logger.info("Fetching user account...")
    stmt = select(Account).where(Account.id == account_id)

    if not lazy:
        stmt = stmt.options(
            selectinload(Account.account_videos).selectinload(AccountVideo.video)
        )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


def get_account_by_id_sync(db: Session, account_id: str):
    stmt = select(Account).where(Account.id == account_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()
