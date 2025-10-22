from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger, validate_video_id
from core.constants import (
    RESP_400_INVALID_YT_ID,
    RESP_401_NOT_AUTHENTICATED,
    RESP_403_ACCOUNT_NOT_APPROVED,
)
from crud import create_conversation, get_conversation_by_user_and_video
from schemas import ConversationCreate, ConversationRequest, ConversationResponse

router = APIRouter()

# --------------------------------------------- GET ----------------------------------------------


@router.get(
    "/{video_id}",
    response_model=ConversationResponse,
    description="Returns the conversation for the authenticated user's account and the given video.",
    responses={
        400: RESP_400_INVALID_YT_ID,
        401: RESP_401_NOT_AUTHENTICATED,
        403: RESP_403_ACCOUNT_NOT_APPROVED,
        404: {"description": "Conversation not found"},
    },
)
async def get_conversation(
    video_id: str,
    auth0_user=Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    validate_video_id(video_id)

    logger.info(f"Fetching conversation...")
    conversation = await get_conversation_by_user_and_video(
        db, auth0_user.sub, video_id, lazy=False
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    return conversation


# -------------------------------------------- POST ----------------------------------------------


@router.post(
    "/",
    response_model=ConversationResponse,
    description="Creates a conversation for the authenticated user's account and the given video.",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: RESP_400_INVALID_YT_ID,
        401: RESP_401_NOT_AUTHENTICATED,
        403: {"description": "Account not approved"},
    },
)
async def post_conversation(
    payload: ConversationRequest,
    auth0_user=Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    video_id = payload.video_id
    validate_video_id(video_id)

    logger.info("Creating conversation...")
    conversation = await get_conversation_by_user_and_video(
        db, auth0_user.sub, video_id
    )

    if conversation is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Conversation already exists"
        )

    conversation_data = ConversationCreate(account_id=auth0_user.sub, video_id=video_id)
    conversation = await create_conversation(db, conversation_data)
    return ConversationResponse(id=conversation.id, messages=[])
