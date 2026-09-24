from typing import Any

from main.tools.base import Tool
from main.tools.protocol import ToolCall, ToolResult
import logging

logger = logging.getLogger(__name__)

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}


    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")

        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as e:
            raise ValueError(f"Unknown tool: {name}")

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def execute(self, call: ToolCall) -> ToolResult:
        """
            Fetch a tool, if it exists in the registry and execute it.
            Returns a generalised tool call result.
            this allows the tool registry to own the complete lifecycle of finding and exeucting a tool call
        """
        try:
            # get the tool
            tool = self.get(call.tool_name)
            # execute the tool
            result = tool.execute(**call.arguments)

            logger.info(f"Executed tool call: {call}")
            return ToolResult(
                tool_name=call.tool_name,
                result=result
            )
        except Exception as e:
            logger.exception(f"Encountered an exception while executing tool call to: {call.tool_name} with arguments: {call.arguments}: {e}")
            return ToolResult(
                tool_name=call.tool_name,
                error=str(e)
            )

    # Automatically extract descriptions of tools into a block to inject into prompt
    # Similar to how list tools call will work and be used to inject inot prompt in MCP
    def describe_tools(self) -> str:
        return "\n".join(
            f"- {tool.name} : {tool.description}"
            for tool in self.list_tools()
        )

    