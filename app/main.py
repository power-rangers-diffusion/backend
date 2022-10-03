from uuid import uuid4

from fastapi import FastAPI

from app.response_schemas.generate_image import GenerateImageResponse
from app.request_schemas.generate_image import GenerateImageRequest

app = FastAPI()


@app.post("/generate-image", response_model=GenerateImageResponse)
def generate_image(rq: GenerateImageRequest):
    return GenerateImageResponse(request_id=uuid4())
