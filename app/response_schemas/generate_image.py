from uuid import UUID

from pydantic import BaseModel


class GenerateImageResponse(BaseModel):
    request_id: UUID
