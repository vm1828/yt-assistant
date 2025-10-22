from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_current_account, get_db, logger
from core.exceptions import (
    EXC_400_INVALID_YT_ID,
    EXC_401_NOT_AUTHENTICATED,
    EXC_403_ACCOUNT_NOT_APPROVED,
    EXC_404_CONV_NOT_ADDED,
    create_responses,
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
    responses=create_responses(
        EXC_400_INVALID_YT_ID,
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_404_CONV_NOT_ADDED,
    ),
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
        raise EXC_404_CONV_NOT_ADDED

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
