import logging

from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from app.config import settings
from app.tools.knowledge_search import search_knowledge_base
from app.tools.calculator import calculator

logger = logging.getLogger(__name__)

REACT_PROMPT = PromptTemplate.from_template("""Answer the following question as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")


def build_agent(max_iterations: int | None = None) -> AgentExecutor:
    llm = ChatOpenAI(
        model=settings.agent_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )

    tools = [search_knowledge_base, calculator]

    agent = create_react_agent(llm=llm, tools=tools, prompt=REACT_PROMPT)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        max_iterations=max_iterations or settings.max_iterations,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )


def run_agent(task: str, max_iterations: int | None = None) -> dict:
    executor = build_agent(max_iterations)

    try:
        result = executor.invoke({"input": task})
    except Exception as e:
        logger.exception("agent execution failed")
        return {
            "result": f"Agent failed: {e}",
            "steps": [],
            "iterations": 0,
        }

    steps = []
    for action, observation in result.get("intermediate_steps", []):
        steps.append({
            "tool": action.tool,
            "input": str(action.tool_input),
            "output": str(observation),
        })

    return {
        "result": result.get("output", ""),
        "steps": steps,
        "iterations": len(steps),
    }
