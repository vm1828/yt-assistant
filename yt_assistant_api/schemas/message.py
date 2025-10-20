from pydantic import BaseModel, ConfigDict


class MessageRead(BaseModel):
    user_message: str
    ai_response: str | None

    model_config = ConfigDict(from_attributes=True)
