from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.account import Account
from schemas.account import AccountCreate


def create_account(db: Session, data: AccountCreate):
    account = Account(id=data.id)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_account_by_id_sync(db: Session, account_id: str):
    stmt = select(Account).where(Account.id == account_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


async def get_account_by_id_async(db: AsyncSession, account_id: str):
    stmt = select(Account).where(Account.id == account_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
