# Embedding Service

FastAPI service that generates vector embeddings using sentence-transformers and stores them in PostgreSQL with pgvector. Also runs a Kafka consumer that processes incoming document chunks automatically.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/embed` | Generate embeddings for a list of texts |
| POST | `/api/v1/search` | Semantic search over stored embeddings |
| GET | `/api/v1/health` | Health check |

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Test

```bash
pytest tests/
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Model for embeddings |
| `EMBEDDING_DIMENSION` | `384` | Vector dimension |
| `POSTGRES_HOST` | `localhost` | Database host |
| `POSTGRES_PORT` | `5432` | Database port |
| `POSTGRES_USER` | `rag_user` | Database user |
| `POSTGRES_PASSWORD` | `rag_pass` | Database password |
| `POSTGRES_DB` | `rag_platform` | Database name |
| `KAFKA_BROKERS` | `localhost:9092` | Kafka bootstrap servers |
