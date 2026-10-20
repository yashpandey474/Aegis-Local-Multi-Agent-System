from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from main.planning.models import Plan
from datetime import datetime, timezone
from uuid import uuid4

"""
Orchestrator controls the execution of a plan. It keeps track of the execution state, including the results of each step.
"""

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ExecutionStatus(StrEnum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class EventType(StrEnum):
    EXECUTION_STARTED = "execution.started"
    PLAN_CREATED = "plan.created"
    STEP_STARTED = "step.started"
    STEP_SUCCEEDED = "step.succeeded"
    STEP_FAILED = "step.failed"
    EXECUTION_SUCCEEDED = "execution.succeeded"
    EXECUTION_FAILED = "execution.failed"


@dataclass(frozen=True)
class ExecutionEvent:
    """ 
    Events gives us an inspectable timeline 
    without needing to infer what happened from the final answer.
    """
    timestamp: datetime
    event_type: EventType
    message: str
    step_id: int | None = None
    duration_seconds: float | None = None


@dataclass(frozen=True)
class StepResult:
    step_id: int
    success: bool
    output: Any = None
    error: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    duration_seconds: float | None = None


@dataclass
class ExecutionState:
    task: str
    plan: Plan
    started_at: datetime = field(default_factory=utc_now)
    finished_at: datetime | None = None
    duration_seconds: float | None = None
    run_id: str = field(default_factory=lambda: str(uuid4()))
    results: list[StepResult] = field(default_factory=list)
    events: list[ExecutionEvent] = field(default_factory=list)
   
    @property
    def success(self) -> bool:
        return self.status == ExecutionStatus.SUCCEEDED
    

    @property
    def final_output(self) -> Any:
        if not self.success or not self.results:
            return None

        return self.results[-1].output # return result of last step