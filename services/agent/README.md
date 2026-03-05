# Agent Service

AI agent with tool-calling capabilities using LangChain's ReAct pattern. Can search the knowledge base and perform calculations as part of multi-step reasoning.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/agent/run` | Run agent with a task |
| GET | `/api/v1/health` | Health check |

## Available Tools

- **search_knowledge_base** - Semantic search over stored documents via the embedding service
- **calculator** - Safe math expression evaluator

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | Required for LLM calls |
| `AGENT_MODEL` | `gpt-4` | LLM model for agent reasoning |
| `MAX_ITERATIONS` | `10` | Max reasoning steps |
| `EMBEDDING_SERVICE_URL` | `http://localhost:8001` | Embedding service URL |
