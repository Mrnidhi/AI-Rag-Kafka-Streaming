import httpx
from langchain.tools import tool

from app.config import settings


@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base for relevant documents.
    Use this when you need to find information from company documents,
    technical docs, or any stored knowledge."""
    try:
        response = httpx.post(
            f"{settings.embedding_service_url}/api/v1/search",
            json={"query": query, "top_k": 5, "threshold": 0.6},
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return "No relevant documents found."

        parts = []
        for r in results:
            score = r.get("score", 0)
            content = r.get("content", "")
            parts.append(f"[score={score:.2f}] {content}")

        return "\n\n".join(parts)

    except Exception as e:
        return f"Knowledge base search failed: {e}"
