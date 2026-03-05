from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    task: str = Field(..., min_length=1)
    max_iterations: int | None = None


class AgentStep(BaseModel):
    tool: str
    input: str
    output: str


class AgentResponse(BaseModel):
    result: str
    steps: list[AgentStep]
    iterations: int
