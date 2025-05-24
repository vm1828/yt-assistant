from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class VideoRequest(BaseModel):
    id: str


class VideoCreate(BaseModel):
    id: str
    title: str
    transcript_text: str


class VideoResponse(BaseModel):
    id: str
    title: str

    model_config = ConfigDict(from_attributes=True)


class VideosResponse(BaseModel):
    videos: Optional[List[VideoResponse]] = []

    model_config = ConfigDict(from_attributes=True)
