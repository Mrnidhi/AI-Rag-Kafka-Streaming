# ADR-001: Vector Database Selection

## Status
Accepted

## Context
Need a vector database to store and retrieve embeddings efficiently for RAG queries with sub-300ms p95 latency.

## Decision
Use **pgvector** as primary choice with **Milvus** as optional alternative.

### Rationale for pgvector:
- Native PostgreSQL extension (operational simplicity)
- ACID guarantees for metadata consistency
- Sufficient performance for <1M vectors
- Lower operational overhead
- Easy backup/restore with existing PostgreSQL tools

### When to use Milvus:
- Scale beyond 10M vectors
- Need GPU-accelerated similarity search
- Multi-collection complex hierarchies
- Dedicated vector search infrastructure

## Consequences

**Positive:**
- Simplified infrastructure
- Single database for vectors + metadata
- Mature PostgreSQL ecosystem

**Negative:**
- May need migration to Milvus at scale
- Limited GPU acceleration

## Implementation
- Use pgvector with HNSW index for similarity search
- Monitor query latency and scale triggers
