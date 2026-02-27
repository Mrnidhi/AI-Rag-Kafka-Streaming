# Ingestion Service

Document ingestion service written in Go. Accepts documents via REST API, splits them into chunks, and publishes to Kafka for downstream processing.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/ingest` | Ingest document via JSON body |
| POST | `/api/v1/ingest/upload` | Upload a file (text/markdown) |
| GET | `/api/v1/health` | Health check |

## Run

```bash
go run cmd/server/main.go
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PORT` | `8000` | Server port |
| `KAFKA_BROKERS` | `localhost:9092` | Kafka bootstrap servers |
| `KAFKA_TOPIC_DOCUMENTS` | `documents.raw` | Target Kafka topic |
| `MAX_FILE_SIZE_MB` | `50` | Max upload size |
| `CHUNK_SIZE` | `512` | Characters per chunk |
| `CHUNK_OVERLAP` | `64` | Overlap between chunks |
