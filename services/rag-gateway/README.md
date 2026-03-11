# RAG Gateway

Spring Boot API gateway that ties together retrieval and LLM generation. Receives user questions, fetches relevant context from the embedding service, sends the context + question to an LLM, and returns the answer with source references.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/query` | Ask a question (RAG pipeline) |
| GET | `/api/v1/health` | Health check |
| GET | `/actuator/prometheus` | Prometheus metrics |

## Run

```bash
./gradlew bootRun
```

## Test

```bash
./gradlew test
```

## Configuration

All config is in `src/main/resources/application.yml` and can be overridden with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PORT` | `8080` | Server port |
| `EMBEDDING_SERVICE_URL` | `http://localhost:8001` | Embedding service base URL |
| `OPENAI_API_KEY` | - | OpenAI API key |
| `LLM_MODEL` | `gpt-4` | LLM model name |
| `REDIS_HOST` | `localhost` | Redis host |
| `RAG_TOP_K` | `5` | Number of chunks to retrieve |
| `CACHE_ENABLED` | `true` | Enable Redis response caching |
