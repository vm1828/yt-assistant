from typing import List
from pydantic import BaseModel, ConfigDict


class VideoCreate(BaseModel):
    id: str
    title: str


class VideoRead(BaseModel):
    id: str
    title: str
    model_config: ConfigDict = {"from_attributes": True}


class VideoReadList(BaseModel):
    videos: List[VideoRead]
    model_config: ConfigDict = {"from_attributes": True}
