"""
Abstraction for the UI wehere dependencies are wired together

UI -> Application Factory -> Orchestrator
"""

from main.agents.analyst import AnalystAgent
from main.agents.base import Agent
from main.agents.registry import AgentRegistry
from main.llm.ollama import LocalLLM
from main.orchestration.orchestrator import Orchestrator
from main.planning.planner import Planner
from main.tools.calculator import CalculatorTool
from main.tools.registry import ToolRegistry
from main.tools.string_length import StringLengthTool
import logging

logger = logging.getLogger(__name__)

def initialise_tool_registry(tools: ToolRegistry):
    tools.register(CalculatorTool())
    tools.register(StringLengthTool())


def initialise_agent_registry(agent_registry: AgentRegistry, agents: list[Agent]):
    for agent in agents:
        agent_registry.register(agent)

    logger.info(f"Registered: {len(agents)} agents")

def build_orchestrator() -> Orchestrator:
    llm = LocalLLM()

    tools = ToolRegistry()
    initialise_tool_registry(tools)

    analyst = AnalystAgent(
        llm=llm,
        tools=tools
    )
    agent_registry = AgentRegistry()
    initialise_agent_registry(agent_registry=agent_registry, agents=[analyst])

    planner = Planner(llm=llm)

    return Orchestrator(
        planner=planner,
        analyst=analyst,
        agent_registry=agent_registry
    )