"""
Abstraction for the UI wehere dependencies are wired together

UI -> Application Factory -> Orchestrator
"""

from main.agents.analyst import AnalystAgent
from main.llm.ollama import LocalLLM
from main.orchestration.orchestrator import Orchestrator
from main.planning.planner import Planner
from main.tools.calculator import CalculatorTool
from main.tools.registry import ToolRegistry
from main.tools.string_length import StringLengthTool


def initialise_tool_registry(tools: ToolRegistry):
    tools.register(CalculatorTool())
    tools.register(StringLengthTool())

def build_orchestrator() -> Orchestrator:
    llm = LocalLLM()

    tools = ToolRegistry()
    initialise_tool_registry(tools)

    analyst = AnalystAgent(
        llm=llm,
        tools=tools
    )

    planner = Planner(llm=llm)

    return Orchestrator(
        planner=planner,
        analyst=analyst
    )