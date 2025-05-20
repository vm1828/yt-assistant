from pydantic import BaseModel, ConfigDict


class TranscriptResponse(BaseModel):
    video_id: str
    transcript_text: str
    
    model_config = ConfigDict(from_attributes=True)
