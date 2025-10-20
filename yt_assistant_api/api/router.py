from fastapi import APIRouter

from api.routes import account, conversation, message, summary, transcript, video

api_router = APIRouter()

api_router.include_router(account.router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(video.router, prefix="/videos", tags=["Videos"])
api_router.include_router(
    transcript.router, prefix="/transcripts", tags=["Transcripts"]
)
api_router.include_router(summary.router, prefix="/summaries", tags=["Summaries"])
api_router.include_router(
    conversation.router, prefix="/conversations", tags=["Conversations"]
)
api_router.include_router(message.router, prefix="/messages", tags=["Messages"])
