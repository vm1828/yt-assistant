from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import get_current_account, get_db_sync, logger
from schemas import Auth0Payload, AccountCreate, AccountResponse
from crud import create_account, get_account_by_id_sync

router = APIRouter()


@router.get(
    "/",
    response_model=AccountResponse,
    description="Returns the authenticated user's account details. Must be authenticated via Auth0.",
)
def get_authenticated_user(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: Session = Depends(get_db_sync),
):
    logger.info("Fetching user account...")
    account_id = auth0_user.sub
    db_user = get_account_by_id_sync(db, account_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return db_user


@router.post(
    "/",
    response_model=AccountResponse,
    description="Creates a new account for the authenticated user if one does not exist.",
)
def create_authenticated_user_account(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: Session = Depends(get_db_sync),
):
    logger.info("Creating new user account...")
    account_id = auth0_user.sub
    db_user = get_account_by_id_sync(db, account_id)

    if db_user is not None:
        raise HTTPException(status_code=409, detail="Account already exists")

    account_data = AccountCreate(id=account_id)
    db_user = create_account(db, account_data)
    return db_user
