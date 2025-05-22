from uuid import UUID
from pydantic import BaseModel, ConfigDict


class SummaryCreate(BaseModel):
    summary_text: str
    transcript_id: UUID


class SummaryResponse(BaseModel):
    video_id: str
    summary_text: str

    model_config = ConfigDict(from_attributes=True)
