import os

from celery import Celery

redis_url = os.getenv("REDIS_URL")
celery_app = Celery("yt_assistant_api_client", broker=redis_url)


def dispatch_transcript_embedding_task(video_id: str):
    celery_app.send_task("tasks.embed.process_transcript_embedding", args=[video_id])
    return {"status": "queued transcript embedding"}
