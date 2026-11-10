from dataclasses import dataclass
from typing import Any

@dataclass
class ToolCall:
    """Represents the request to execute a tool"""
    tool_name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    """Represents the outcome of a tool call"""
    tool_name: str
    result: Any = None
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None