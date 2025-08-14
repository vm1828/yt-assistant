import logging
import os
import uuid
from dataclasses import asdict, dataclass
from typing import Tuple

from celery import Celery
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from psycopg2 import connect
from psycopg2.extras import execute_values

# ---------------------------- Logging ----------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------- Config ----------------------------
redis_url = os.getenv("REDIS_URL")
db_url = os.getenv("POSTGRES_URL")
google_api_key = os.getenv("GOOGLE_API_KEY")

CHUNK_SIZE = 1024
CHUNK_OVERLAP = 100

celery_app = Celery("yt_assistant_emb_worker", broker=redis_url)

# ---------------------------- Model ----------------------------
# lazy init of embedding model
_emb_model = None


def get_emb_model():
    global _emb_model
    if _emb_model is None:
        _emb_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", google_api_key=google_api_key
        )
    return _emb_model


# ---------------------------- Task ----------------------------


@dataclass
class ProcessTranscriptEmbeddingResult:
    video_id: str
    transcript_id: str
    chunk_count: int


def process_transcript_embedding_logic(
    video_id: str,
    conn,
    emb_model,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> Tuple[str, int]:
    """
    Core embedding workflow:
    - Fetch transcript from DB
    - Chunk it
    - Store chunks
    - Generate embeddings
    - Store embeddings
    Returns: (transcript_id, chunk_count)
    """
    with conn.cursor() as cur:
        # 1. Fetch transcript
        cur.execute(
            "SELECT id, transcript_text FROM transcript WHERE video_id = %s",
            (video_id,),
        )
        transcript_id, transcript_text = cur.fetchone()

        # 2. Chunk transcript
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
        )
        chunks = splitter.split_text(transcript_text)
        logger.info(f"Transcript split into {len(chunks)} chunks")

        # 3. Insert chunks
        chunk_records = [
            (str(uuid.uuid4()), transcript_id, chunk_text, i)
            for i, chunk_text in enumerate(chunks)
        ]
        execute_values(
            cur,
            """
            INSERT INTO transcript_chunk (id, transcript_id, chunk_text, chunk_index)
            VALUES %s
            """,
            chunk_records,
        )
        logger.info(f"Inserted {len(chunk_records)} transcript chunks")

        # 4. Generate embeddings
        vectors = emb_model.embed_documents(chunks)

        # 5. Insert embeddings
        embedding_records = [
            (str(uuid.uuid4()), chunk_id, vector)
            for (chunk_id, _, _, _), vector in zip(chunk_records, vectors)
        ]
        execute_values(
            cur,
            """
            INSERT INTO embedding (id, transcript_chunk_id, embedding)
            VALUES %s
            """,
            embedding_records,
        )

    conn.commit()
    return transcript_id, len(chunks)


@celery_app.task(
    bind=True,
    name="tasks.embed.process_transcript_embedding",
    autoretry_for=(Exception,),
    retry_backoff=15,
    retry_backoff_max=60,
    retry_kwargs={"max_retries": 3},
)
def process_transcript_embedding(
    self, video_id: str
) -> ProcessTranscriptEmbeddingResult:
    logger.info(
        f"Task run id: {self.request.id} - Embedding transcript for video {video_id}"
    )
    with connect(db_url) as conn:
        transcript_id, chunk_count = process_transcript_embedding_logic(
            video_id=video_id,
            conn=conn,
            emb_model=get_emb_model(),
        )
    logger.info(f"Stored {chunk_count} embeddings for transcript {transcript_id}")
    result = ProcessTranscriptEmbeddingResult(video_id, transcript_id, chunk_count)
    return asdict(result)
