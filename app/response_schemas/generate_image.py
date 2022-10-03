from pydantic import BaseModel


class GenerateImageResponse(BaseModel):
    request_id: str
