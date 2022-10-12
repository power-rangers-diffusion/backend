from pydantic import BaseModel

class GenerateImageResponse(BaseModel):
    message_id: str
