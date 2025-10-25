from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger, validate_video_id
from core.exceptions import (
    EXC_400_INVALID_YT_ID,
    EXC_401_NOT_AUTHENTICATED,
    EXC_403_ACCOUNT_NOT_APPROVED,
    EXC_404_CONV_NOT_FOUND,
    EXC_409_CONV_ALREADY_EXISTS,
    create_responses,
)
from crud import create_conversation, get_conversation_by_user_and_video
from schemas import ConversationCreate, ConversationRequest, ConversationResponse

router = APIRouter()

# --------------------------------------------- GET ----------------------------------------------


@router.get(
    "/{video_id}",
    response_model=ConversationResponse,
    description="Returns the conversation for the authenticated user's account and the given video.",
    responses=create_responses(
        EXC_400_INVALID_YT_ID,
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_404_CONV_NOT_FOUND,
    ),
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
        raise EXC_404_CONV_NOT_FOUND

    return conversation


# -------------------------------------------- POST ----------------------------------------------


@router.post(
    "/",
    response_model=ConversationResponse,
    description="Creates a conversation for the authenticated user's account and the given video.",
    status_code=status.HTTP_201_CREATED,
    responses=create_responses(
        EXC_400_INVALID_YT_ID,
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_409_CONV_ALREADY_EXISTS,
    ),
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
        raise EXC_409_CONV_ALREADY_EXISTS

    conversation_data = ConversationCreate(account_id=auth0_user.sub, video_id=video_id)
    conversation = await create_conversation(db, conversation_data)
    return ConversationResponse(id=conversation.id, video_id=video_id, messages=[])
