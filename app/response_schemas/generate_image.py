from pydantic import BaseModel

class SimilarityResult(BaseModel):
    id: str
    caption: str
    url: str
    similarity: float

class GenerateImageResponse(BaseModel):
    message_id: str,
    gen_image: str,
    similarity_results: List[SimilarityResult]
