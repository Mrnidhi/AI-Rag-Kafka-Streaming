# ADR-002: Kafka for Real-Time Streaming

## Status
Accepted

## Context
Need real-time knowledge updates without batch re-indexing. System must handle continuous document ingestion and immediate availability.

## Decision
Use **Apache Kafka** as the central streaming platform.

## Rationale
- Industry-standard for event streaming
- High throughput (50k+ msg/sec)
- Durability and replay capabilities
- Rich ecosystem (Schema Registry, Connect, Streams)
- Decouples producers and consumers

## Key Topics
- `documents.raw` - Document ingestion events
- `embeddings.ready` - Processed embeddings
- `events.live` - Real-time business events
- `rag.query.logs` - Query analytics

## Consequences

**Positive:**
- Real-time knowledge updates
- Event sourcing capabilities
- Service decoupling
- Scalable ingestion pipeline

**Negative:**
- Additional operational complexity
- Requires ZooKeeper (moving to KRaft)
- Learning curve for team

## Alternatives Considered
- RabbitMQ: Less suited for streaming/replay
- Pulsar: Less mature ecosystem
- Direct DB polling: Doesn't scale
