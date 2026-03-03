from fastapi import APIRouter, HTTPException

from app.models.schemas import SearchRequest, SearchResponse, SearchResult
from app.services.embedder import embedding_service
from app.services.vector_store import vector_store

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def semantic_search(req: SearchRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="query cannot be empty")

    query_embedding = embedding_service.embed_single(req.query)
    raw_results = vector_store.search(
        query_embedding=query_embedding,
        top_k=req.top_k,
        threshold=req.threshold,
    )

    results = [SearchResult(**r) for r in raw_results]

    return SearchResponse(
        results=results,
        query=req.query,
        total=len(results),
    )
