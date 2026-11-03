from main.agents.base import Agent
from main.agents.results import AgentResult
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

    def run_tool_call_followup(self, task: str, response: LLMResponse) -> LLMResponse:
            # LLM Should decide: I need the calculator
            try:
                # Parse LLM JSON response to a tool call
                tool_call: ToolCall = ToolCallParser.parse(response.content)
            except ValueError:
                 logger.debug("LLM did not return a valid tool call")
                 return response
            
            # Execute the tool call            
            result: ToolResult = self.tools.execute(tool_call)

            if not result.success:
                 raise RuntimeError(
                    f"Tool '{tool_call.tool_name}' failed: {result.error}"
                 )
            
            follow_up_prompt = ANALYST_AGENT_FOLLOW_UP_PROMPT.format(
                task=task,
                tool_name=tool_call.tool_name,
                arguments=tool_call.arguments,
                result=result.result
            )

            # no more tool calls allowed (should later be configured somewhere?)
            follow_up_response = self.llm.generate(follow_up_prompt)
            
            logger.info(f"Follow up response from LLM: {follow_up_response}")
            return follow_up_response

    def run(self, task: str) -> LLMResponse:
        prompt = ANALYST_AGENT_PROMPT.format(
            task=task,
            tools_description=self.tools.describe_tools()
        )
        llm_response: LLMResponse = self.llm.generate(prompt)
        logger.info(f"In {self.name}: Response from LLM: {llm_response.content}")

        # we currently allow just one tool call
        llm_final_response: LLMResponse =  self.run_tool_call_followup(
            task=task,
            response=llm_response
        )

        return AgentResult(
             name=self.name,
             output=llm_final_response.content,
             metadata={"llm_model": llm_final_response.model}
        )