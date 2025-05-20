from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core import get_current_account, get_db_sync, logger
from schemas import Auth0Payload, AccountCreate, AccountResponse
from crud import create_account, get_account_by_id_sync

router = APIRouter()


@router.get(
    "/me",
    response_model=AccountResponse,
    description="""Returns the authenticated user's account details. User must be authenticated via Auth0.
    If no local account exists, one will be created automatically.""",
)
def get_authenticated_user(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: Session = Depends(get_db_sync),
):
    logger.info("Fetching user account...")  # Check if account exists in the database
    account_id = auth0_user.sub
    db_user = get_account_by_id_sync(db, account_id)

    if db_user is None:
        logger.info("Adding new user account...")
        account_data = AccountCreate(id=account_id)
        db_user = create_account(db, account_data)

    return db_user
