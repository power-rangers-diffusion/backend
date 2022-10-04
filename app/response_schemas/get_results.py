from pydantic import BaseModel


class GetResultsResponse(BaseModel):
    generated_image: str
