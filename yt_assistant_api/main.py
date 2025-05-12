from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.router import api_router

app = FastAPI(
    title=f"yt-assistant-{settings.ENV}",
    description="Web application designed to help users summarize YouTube video transcripts and extract valuable insights through question answering and reasoning",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
