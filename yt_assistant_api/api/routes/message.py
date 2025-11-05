from config import settings
from core import get_current_account, get_db, logger
from core.exceptions import (
    EXC_401_NOT_AUTHENTICATED,
    EXC_403_ACCOUNT_NOT_APPROVED,
    EXC_404_CONV_NOT_ADDED,
    create_responses,
)
from crud import (
    create_message,
    get_conversation_by_id,
    get_top_similar_chunks_for_video,
)
from fastapi import APIRouter, Depends, status
from schemas import MessageCreate, MessageRequest, MessageResponse
from services import (
    get_ai_response,
    get_emb_adapter,
    get_user_msg_w_history,
    should_use_context,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# -------------------------------------------- POST ----------------------------------------------


@router.post(
    "/",
    response_model=MessageResponse,
    description="Post a new message within a conversation.",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_account)],
    responses=create_responses(
        EXC_401_NOT_AUTHENTICATED,
        EXC_403_ACCOUNT_NOT_APPROVED,
        EXC_404_CONV_NOT_ADDED,
    ),
)
async def post_message(
    payload: MessageRequest,
    db: AsyncSession = Depends(get_db),
):
    user_msg, conversation_id = (
        payload.user_message,
        payload.conversation_id,
    )

    logger.info("Retrieve conversation from db...")
    conversation = await get_conversation_by_id(db, conversation_id, lazy=False)
    if not conversation:
        raise EXC_404_CONV_NOT_ADDED

    logger.info("Preparing context...")
    # TODO Imporove efficiency and avoid limitations (limit messages / isolated embedding spaces / summarized history etc.)
    user_msg_w_history = get_user_msg_w_history(user_msg, conversation)
    context = ""
    if await should_use_context(user_msg):
        emb_adapter = get_emb_adapter(settings.ENV == "local")
        query_embedding = await emb_adapter.embed([user_msg])
        chunks = await get_top_similar_chunks_for_video(
            db, conversation.video_id, query_embedding[0]
        )
        context = "\n\n".join(chunks)

    logger.info("Trying to get response from LLM...")
    ai_response = await get_ai_response(user_msg_w_history, context)

    logger.info("Writing message to db...")
    data = MessageCreate(
        conversation_id=conversation_id,
        user_message=user_msg,
        ai_response=ai_response,
    )
    message = await create_message(db, data)

    return message
