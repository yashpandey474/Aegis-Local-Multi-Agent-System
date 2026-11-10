from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class AgentResult:
    agent_name: str # the agent that generated the result
    output: str # will the output always be a string?
    metadata: dict[str, Any] = field(default_factory=dict)
    artifacts: tuple[dict[str, Any], ...] = () # step-by-step artifacts like tool calls