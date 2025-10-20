from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger
from crud import create_message
from schemas import MessageCreate, MessageRequest, MessageResponse
from services import get_ai_response

router = APIRouter()

# -------------------------------------------- POST ----------------------------------------------


@router.post(
    "/",
    response_model=MessageResponse,
    description="Post a new message within a conversation.",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_account)],
    responses={
        400: {"description": "Invalid YouTube video ID"},
        401: {"description": "Not authenticated"},
        403: {"description": "Account not approved"},
    },  # TODO refactor, remove duplications in responses documentation
)
async def post_message(
    payload: MessageRequest,
    db: AsyncSession = Depends(get_db),
):
    print(payload)
    user_message, conversation_id = (
        payload.user_message,
        payload.conversation_id,
    )

    logger.info("Trying to get response from LLM...")
    ai_response = await get_ai_response(
        user_message
    )  # TODO replace with context-aware logic

    logger.info("Writing message to db...")
    data = MessageCreate(
        conversation_id=conversation_id,
        user_message=user_message,
        ai_response=ai_response,
    )
    message = await create_message(db, data)

    return message
