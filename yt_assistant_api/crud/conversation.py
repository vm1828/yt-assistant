from models import Conversation
from schemas import ConversationCreate
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def get_conversation_by_user_and_video(
    db: AsyncSession, account_id: str, video_id: str, lazy: bool = True
) -> Conversation | None:
    stmt = select(Conversation).where(
        Conversation.account_id == account_id, Conversation.video_id == video_id
    )

    if not lazy:
        stmt = stmt.options(selectinload(Conversation.messages))

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_conversation_by_id(
    db: AsyncSession, conversation_id: str, lazy: bool = True
) -> Conversation | None:
    stmt = select(Conversation).where(Conversation.id == conversation_id)

    if not lazy:
        stmt = stmt.options(selectinload(Conversation.messages))

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_conversation(
    db: AsyncSession, data: ConversationCreate
) -> Conversation:
    """Create conversation"""
    conversation = Conversation(**data.model_dump())
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation

# ---------------------------------- RAG helpers ----------------------------------

async def get_top_similar_chunks_for_video(
    db: AsyncSession, video_id: str, query_embedding, n_chunks: int = 3
) -> list[str]:
    """Retrieve top-K transcript chunks for a specific query by similarity."""
    query_embedding = "[" + ", ".join(str(x) for x in query_embedding) + "]"
    sql = text("""
        SELECT tc.chunk_text, (e.embedding <#> :query_embedding) AS distance
        FROM embedding e
        JOIN transcript_chunk tc ON e.transcript_chunk_id = tc.id
        JOIN transcript t ON tc.transcript_id = t.id
        WHERE t.video_id = :video_id
        ORDER BY e.embedding <#> :query_embedding
        LIMIT :n_chunks
    """)
    result = await db.execute(
        sql,
        {
            "video_id": video_id,
            "query_embedding": query_embedding,
            "n_chunks": n_chunks,
        },
    )
    return [row[0] for row in result.fetchall()]

