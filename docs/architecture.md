# Architecture

## Services

| Service | Language | Port | Role |
|---------|----------|------|------|
| Ingestion | Go (Fiber) | 8000 | Accepts documents, chunks them, publishes to Kafka |
| Embedding | Python (FastAPI) | 8001 | Generates embeddings, stores in pgvector, runs Kafka consumer |
| RAG Gateway | Java (Spring Boot) | 8080 | Receives questions, retrieves context, calls LLM, returns answers |
| Agent | Python (FastAPI) | 8002 | Multi-step reasoning with tool calling (LangChain ReAct) |

## Data Flow

1. User uploads a document via the ingestion service
2. Document is split into chunks and published to Kafka (`documents.raw`)
3. Embedding service consumes chunks, generates vector embeddings, stores in PostgreSQL (pgvector)
4. User asks a question via the RAG gateway
5. Gateway calls the embedding service to find the most relevant chunks
6. Gateway sends the retrieved context + question to OpenAI
7. LLM generates an answer grounded in the context
8. Response is returned with source references

## Infrastructure

- **PostgreSQL + pgvector** -- Document metadata and vector storage
- **Kafka** -- Async message passing between ingestion and embedding
- **Redis** -- Response caching in the RAG gateway
- **Prometheus + Grafana** -- Metrics
- **Jaeger** -- Distributed tracing

## Design Decisions

See `docs/adr/` for architectural decision records.
