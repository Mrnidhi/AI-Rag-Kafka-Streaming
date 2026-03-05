import logging

from fastapi import FastAPI, HTTPException

from app.config import settings
from app.models.schemas import AgentRequest, AgentResponse, AgentStep
from app.agent import run_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

app = FastAPI(
    title="Agent Service",
    version="1.0.0",
)


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "service": "agent"}


@app.post("/api/v1/agent/run", response_model=AgentResponse)
def run(req: AgentRequest):
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    result = run_agent(
        task=req.task,
        max_iterations=req.max_iterations,
    )

    return AgentResponse(
        result=result["result"],
        steps=[AgentStep(**s) for s in result["steps"]],
        iterations=result["iterations"],
    )
