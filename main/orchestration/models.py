from dataclasses import dataclass, field
from typing import Any

from main.planning.models import Plan

"""
Orchestrator controls the execution of a plan. It keeps track of the execution state, including the results of each step.
"""
@dataclass(frozen=True)
class StepResult:
    step_id: int
    success: bool
    output: Any = None
    error: str | None = None


@dataclass
class ExecutionState:
    task: str
    plan: Plan
    results: list[StepResult] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return all(result.success for result in self.results)

    @property
    def final_output(self) -> Any:
        if not self.results:
            return None

        return self.results[-1].output # return result of last step