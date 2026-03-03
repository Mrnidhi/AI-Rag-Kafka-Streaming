from fastapi import APIRouter, HTTPException

from app.config import settings
from app.models.schemas import EmbedRequest, EmbedResponse
from app.services.embedder import embedding_service

router = APIRouter()


@router.post("/embed", response_model=EmbedResponse)
def generate_embeddings(req: EmbedRequest):
    if not req.texts:
        raise HTTPException(status_code=400, detail="texts list cannot be empty")

    embeddings = embedding_service.embed(req.texts)

    return EmbedResponse(
        embeddings=embeddings,
        model=req.model or settings.embedding_model,
        dimension=settings.embedding_dimension,
    )
