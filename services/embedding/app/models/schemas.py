from pydantic import BaseModel, Field


class EmbedRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1)
    model: str | None = None


class EmbedResponse(BaseModel):
    embeddings: list[list[float]]
    model: str
    dimension: int


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: dict | None = None


class SearchResponse(BaseModel):
    results: list[SearchResult]
    query: str
    total: int
