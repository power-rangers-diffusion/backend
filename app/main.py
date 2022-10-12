import base64
import json
import aioboto3
import botocore

from uuid import uuid4
from io import BytesIO


from fastapi import FastAPI

from app.response_schemas.generate_image import GenerateImageResponse
from app.request_schemas.generate_image import GenerateImageRequest

app = FastAPI()


@app.post("/generate-image", response_model=GenerateImageResponse)
async def generate_image(rq: GenerateImageRequest):
    request_id = str(uuid4())

    async with aioboto3.Session(region_name="us-east-1").resource("sqs") as sqs:
        queue = await sqs.get_queue_by_name(QueueName="inference-request.fifo")

        message_dict = {"prompt": rq.prompt}
        await queue.send_message(
            MessageBody=json.dumps(message_dict),
            MessageGroupId="1",
            MessageDeduplicationId=request_id
        )

    return GenerateImageResponse(request_id=request_id)

@app.get("/results/{request_id}")
async def get_results(request_id: str):
    obj_key = f"{request_id}.json"
    buffer = BytesIO()

    async with aioboto3.Session(region_name="us-east-1").resource("s3") as s3:
        bucket = await s3.Bucket("fsdl-52-images")
        try:
            await bucket.download_fileobj(obj_key, buffer)
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == "404":
                return {}
            else:
                raise err

    return json.loads(buffer.getvalue())