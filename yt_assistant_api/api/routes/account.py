from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger
from core.exceptions import (
    EXC_401_NOT_AUTHENTICATED,
    EXC_403_ACCOUNT_NOT_APPROVED,
    EXC_404_ACC_NOT_FOUND,
    EXC_409_ACC_ALREADY_EXISTS,
    create_responses,
)
from crud import create_account, get_account_by_id
from schemas import AccountCreate, AccountResponse, Auth0Payload

router = APIRouter()

# ------------------------------------------ GET -------------------------------------------


@router.get(
    "/",
    response_model=AccountResponse,
    description="Returns the authenticated user's account details.",
    responses=create_responses(EXC_401_NOT_AUTHENTICATED, EXC_404_ACC_NOT_FOUND),
)
async def get_authenticated_user(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Fetching user account...")
    db_user = await get_account_by_id(db, auth0_user.sub)

    if db_user is None:
        raise EXC_404_ACC_NOT_FOUND

    return db_user


# ------------------------------------------ POST -------------------------------------------


@router.post(
    "/",
    response_model=AccountResponse,
    description="Creates a new account for the authenticated user if one does not exist.",
    status_code=status.HTTP_201_CREATED,
    responses=create_responses(
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_409_ACC_ALREADY_EXISTS,
    ),
)
async def create_authenticated_user_account(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Creating new user account...")
    db_user = await get_account_by_id(db, auth0_user.sub)

    if db_user is not None:
        raise EXC_409_ACC_ALREADY_EXISTS

    account_data = AccountCreate(id=auth0_user.sub)
    db_user = await create_account(db, account_data)
    return db_user
