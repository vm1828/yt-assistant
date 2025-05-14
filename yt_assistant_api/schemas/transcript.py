from pydantic import BaseModel, ConfigDict


class TranscriptRead(BaseModel):
    transcript_text: str
    model_config: ConfigDict = {"from_attributes": True}
