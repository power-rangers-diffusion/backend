import json

import aioboto3

from uuid import uuid4

from fastapi import FastAPI

from app.response_schemas.generate_image import GenerateImageResponse
from app.request_schemas.generate_image import GenerateImageRequest

app = FastAPI()


@app.post("/generate-image", response_model=GenerateImageResponse)
async def generate_image(rq: GenerateImageRequest):
    request_id = str(uuid4())

    async with aioboto3.Session().resource("sqs") as sqs:
        queue = await sqs.get_queue_by_name(QueueName="inference-request.fifo")

        message_dict = {"prompt": rq.prompt}
        await queue.send_message(
            MessageBody=json.dumps(message_dict),
            MessageGroupId="1",
            MessageDeduplicationId=request_id
        )

    return GenerateImageResponse(request_id=request_id)
