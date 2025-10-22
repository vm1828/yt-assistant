from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger
from core.constants import (
    RESP_400_INVALID_YT_ID,
    RESP_401_NOT_AUTHENTICATED,
    RESP_403_ACCOUNT_NOT_APPROVED,
)
from crud import create_message, get_conversation_by_id
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
        400: RESP_400_INVALID_YT_ID,
        401: RESP_401_NOT_AUTHENTICATED,
        403: RESP_403_ACCOUNT_NOT_APPROVED,
        404: {"description": "Conversation is not added yet"},
    },
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

    logger.info("Retrieve conversation from db...")
    conversation = await get_conversation_by_id(db, conversation_id, lazy=False)
    if not conversation:
        raise HTTPException(
            404, "Conversation is not added yet. Please add the conversation first."
        )

    # Create context-aware LLM input
    history = []
    for msg in conversation.messages:
        history.append(f"User: {msg.user_message}")
        history.append(f"Assistant: {msg.ai_response}")
    history.append(f"User: {user_message}")
    # TODO Imporove efficiency and avoid limitations (limit messages / isolated embedding spaces / summarized history etc.)
    context_aware_msg = "\n".join(history)

    logger.info("Trying to get response from LLM...")
    ai_response = await get_ai_response(context_aware_msg)

    logger.info("Writing message to db...")
    data = MessageCreate(
        conversation_id=conversation_id,
        user_message=user_message,
        ai_response=ai_response,
    )
    message = await create_message(db, data)

    return message
