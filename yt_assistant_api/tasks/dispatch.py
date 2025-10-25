from celery import Celery

from config import settings

celery_app = Celery("yt_assistant_api_client", broker=settings.REDIS_URL)


def dispatch_transcript_embedding_task(video_id: str):
    celery_app.send_task("tasks.embed.process_transcript_embedding", args=[video_id])
    return {"status": "queued transcript embedding"}
