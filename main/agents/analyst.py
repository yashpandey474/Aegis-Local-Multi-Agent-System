from main.agents.base import Agent
from main.llm.ollama import LLMResponse, LocalLLM
from main.agents.constants import ANALYST_AGENT_FOLLOW_UP_PROMPT, ANALYST_AGENT_PROMPT
from main.tools import CalculatorTool, ToolRegistry
import logging

logger = logging.getLogger(__name__)

class AnalystAgent(Agent):
    def __init__(
            self,
            llm: LocalLLM,
            tools: ToolRegistry,
        ) -> None:
        super().__init__(
            name="analyst",
            description="Ananlyzes questions and produces structured reasoning and conclusions."
        )
        self.llm = llm
        self.tools = tools

    def run(self, task: str) -> LLMResponse:
        prompt = ANALYST_AGENT_PROMPT.format(task=task)
        response = self.llm.generate(prompt)
        logger.info(f"Response from LLM: {response.content}")

        # LLM Should decide: I need the calculator
        if response.content.startswith("TOOL: calculator"):

            # The tool registry should decide if calculator is a registered tool and the arguments are valid
            expression = self._extract_expression(response.content)
            # This should not sit in the agent, later it'll be an mcp call with
            calculator = self.tools.get("calculator")
            result = calculator.execute(expression=expression)
            
            logger.info(f"Calculator tool invoked with: {expression}. Result: {result}")

            follow_up_prompt = ANALYST_AGENT_FOLLOW_UP_PROMPT.format(
                task=task,
                expression=expression,
                result=result
            )

            follow_up_response = self.llm.generate(follow_up_prompt)
            logger.info(f"Follow up response from LLM: {follow_up_response}")
            return follow_up_response

        return response

    @staticmethod
    def _extract_expression(response: str) -> str:
        for line in response.splitlines():
            if line.startswith("EXPRESSION: "):
                return line.split(":", 1)[1].strip()

        raise ValueError(
            "Calculator tool was requested but no expression was provided."
        )