from pydantic import BaseModel


class GenerateImageRequest(BaseModel):
    prompt: str
