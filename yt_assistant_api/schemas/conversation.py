from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .message import MessageRead


class ConversationRequest(BaseModel):
    video_id: str


class ConversationCreate(BaseModel):
    account_id: str
    video_id: str


class ConversationResponse(BaseModel):
    id: UUID
    messages: Optional[list[MessageRead]] = []

    model_config = ConfigDict(from_attributes=True)
