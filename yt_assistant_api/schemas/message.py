from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MessageRequest(BaseModel):
    conversation_id: UUID
    user_message: str


class MessageCreate(BaseModel):
    conversation_id: UUID
    user_message: str
    ai_response: str | None


class MessageRead(BaseModel):
    user_message: str
    ai_response: str | None

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    ai_response: str | None

    model_config = ConfigDict(from_attributes=True)
