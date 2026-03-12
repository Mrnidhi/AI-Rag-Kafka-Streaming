# Local Development

## Prerequisites

- Docker and Docker Compose
- Go 1.21+
- Python 3.11+
- Java 21
- Make

## Setup

```bash
git clone <repo-url>
cd ai-rag-kafka-streaming-platform
make bootstrap
```

This starts PostgreSQL, Kafka, Redis, and creates Kafka topics.

## Configure

```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

## Run Services

Each service runs separately in its own terminal.

**Ingestion (port 8000):**
```bash
cd services/ingestion
go run cmd/server/main.go
```

**Embedding (port 8001):**
```bash
cd services/embedding
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

**RAG Gateway (port 8080):**
```bash
cd services/rag-gateway
./gradlew bootRun
```

**Agent (port 8002):**
```bash
cd services/agent
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

## Test a Query

```bash
# Ingest a document
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "content": "RAG combines retrieval with generation.", "source": "test"}'

# Wait a few seconds for embedding pipeline to process

# Ask a question
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

## Dashboards

- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Jaeger: http://localhost:16686

## Troubleshooting

**Kafka not starting:** Check ZooKeeper status with `docker-compose logs zookeeper`.

**pgvector errors:** Make sure the init.sql ran: `docker exec rag-postgres psql -U rag_user -d rag_platform -c "SELECT * FROM pg_extension WHERE extname = 'vector';"`.

## Cleanup

```bash
make down
make clean
```
