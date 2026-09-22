from typing import Any

from code.tools.base import Tool
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