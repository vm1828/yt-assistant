from typing import List
from pydantic import BaseModel, ConfigDict


class VideoCreate(BaseModel):
    id: str
    title: str


class VideoResponse(BaseModel):
    id: str
    title: str

    model_config = ConfigDict(from_attributes=True)


class VideosResponse(BaseModel):
    videos: List[VideoResponse]

    model_config = ConfigDict(from_attributes=True)
