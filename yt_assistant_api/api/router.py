from fastapi import APIRouter
from api.routes import account, video, transcript

api_router = APIRouter()

api_router.include_router(account.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(video.router, prefix="/videos", tags=["videos"])
api_router.include_router(
    transcript.router, prefix="/transcripts", tags=["transcripts"]
)
