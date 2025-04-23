from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.db_session import get_db
from core.auth import get_current_account
from schemas.account import Auth0Payload, AccountCreate, AccountRead
from services.account import get_account_by_id, create_account

router = APIRouter()


@router.get(
    "/me",
    response_model=AccountRead,
    description="Returns the authenticated user's account details. User must be authenticated via Auth0. "
    "If no local account exists, one will be created automatically.",
)
def get_authenticated_user(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    account_id = auth0_user.sub
    db_user = get_account_by_id(db, account_id)
    if db_user is None:
        account_data = AccountCreate(id=account_id)
        db_user = create_account(db, account_data)
    return db_user
