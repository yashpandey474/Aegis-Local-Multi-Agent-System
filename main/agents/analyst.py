from main.agents.base import Agent
from main.llm.ollama import LLMResponse, LocalLLM
from main.agents.constants import ANALYST_AGENT_FOLLOW_UP_PROMPT, ANALYST_AGENT_PROMPT
from main.tools import ToolRegistry
import logging

from main.tools import ToolCall, ToolResult
from main.tools.parser import ToolCallParser

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

    def run_tool_call_followup(self, task: str, response_content: str) -> str:
        # LLM Should decide: I need the calculator
        try:
            # Parse LLM JSON response to a tool call
            tool_call: ToolCall = ToolCallParser.parse(response_content)
            # Execute the tool call            
            result: ToolResult = self.tools.execute(tool_call)
            
            follow_up_prompt = ANALYST_AGENT_FOLLOW_UP_PROMPT.format(
                task=task,
                tool_name=tool_call.tool_name,
                arguments=tool_call.arguments,
                result=result.result
            )

            follow_up_response = self.llm.generate(follow_up_prompt)
            logger.info(f"Follow up response from LLM: {follow_up_response}")
            return follow_up_response
        except Exception as e:
            logger.debug("LLM did not return JSON, no tool call")
            return response_content

    def run(self, task: str) -> LLMResponse:
        prompt = ANALYST_AGENT_PROMPT.format(
            task=task,
            tools_description=self.tools.describe_tools()
        )
        response = self.llm.generate(prompt)
        logger.info(f"Response from LLM: {response.content}")

        final_response = self.run_tool_call_followup(
            task=task,
            response_content=response.content
        )

        return final_response