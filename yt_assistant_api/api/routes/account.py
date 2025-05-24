from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from core import get_current_account, logger
from schemas import Auth0Payload, AccountCreate, AccountResponse
from crud import create_account, get_account_by_id_async
from core import get_db_async

router = APIRouter()


@router.get(
    "/",
    response_model=AccountResponse,
    description="Returns the authenticated user's account details. Must be authenticated via Auth0.",
    responses={
        404: {"description": "Account not found"},
    },
)
async def get_authenticated_user(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: AsyncSession = Depends(get_db_async),
):
    logger.info("Fetching user account...")
    db_user = await get_account_by_id_async(db, auth0_user.sub)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )

    return db_user


@router.post(
    "/",
    response_model=AccountResponse,
    description="Creates a new account for the authenticated user if one does not exist.",
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Account already exists"},
    },
)
async def create_authenticated_user_account(
    auth0_user: Auth0Payload = Depends(get_current_account),
    db: AsyncSession = Depends(get_db_async),
):
    logger.info("Creating new user account...")
    db_user = await get_account_by_id_async(db, auth0_user.sub)

    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )

    account_data = AccountCreate(id=auth0_user.sub)
    db_user = await create_account(db, account_data)
    return db_user
