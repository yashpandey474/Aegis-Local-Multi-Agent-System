from dataclasses import dataclass
from typing import Generic, TyeV

T = TypeVar("T")
@dataclass
class ToolCall:
    name: str
    arguments: dict

@dataclass
class ToolResult:
    tool: str
    result: any