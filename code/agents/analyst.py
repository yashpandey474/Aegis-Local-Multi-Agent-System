from code.agents.base import Agent
from code.llm.ollama import LLMResponse, LocalLLM
from code.agents.constants import ANALYST_AGENT_PROMPT
from code.tools.calculator import CalculatorTool
import logging

logger = logging.getLogger(__name__)

class AnalystAgent(Agent):
    def __init__(
            self,
            llm: LocalLLM,
            calculator: CalculatorTool,
        ) -> None:
        super().__init__(
            name="analyst",
            description="Ananlyzes questions and produces structured reasoning and conclusions."
        )
        self.llm = llm
        self.calculator = calculator

    def run(self, task: str) -> LLMResponse:
        prompt = ANALYST_AGENT_PROMPT.format(task=task)
        response = self.llm.generate(prompt)
        logger.info(f"Response from LLM: {response.content}")
        if response.content.startswith("TOOL: calculator"):
            expression = self._extract_expression(response.content)
            result = self.calculator.execute(expression=expression)
            logger.info(f"Calculator tool invoked with: {expression}. Result: {result}")

            follow_up_prompt = f"""You are the Analyst Agent.

                Original task:
                {task}

                You requested the calculator tool.

                Expression:
                {expression}

                Calculator result:
                {result}

                Using this result, provide the final answer to the user.
                Do not mention internal tool execution unless relevant.
            """

            follow_up_response = self.llm.generate(follow_up_prompt)
            logger.info(f"Response from LLM: {follow_up_response}")
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