from sqlalchemy.orm import Session
from models.account import Account
from schemas.account import AccountCreate


def create_account(db: Session, data: AccountCreate):
    account = Account(id=data.id)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_account_by_id(db: Session, account_id: str):
    return db.query(Account).filter(Account.id == account_id).first()
