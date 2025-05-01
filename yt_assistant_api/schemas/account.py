from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    id: str


class AccountRead(BaseModel):
    id: str
    model_config: ConfigDict = {"from_attributes": True}


class Auth0Payload(BaseModel):
    sub: str
