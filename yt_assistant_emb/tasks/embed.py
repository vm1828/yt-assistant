import os

from celery import Celery

redis_url = os.getenv("REDIS_URL")
celery_app = Celery("yt_assistant_rag_worker", broker=redis_url)


@celery_app.task(name="tasks.embed.process_transcript_embedding")
def process_transcript_embedding(video_id: str):
    print(f"Embedding transcript for video {video_id}")
    pass
