from dataclasses import dataclass

@dataclass(frozen=True)
class PlanStep:
    "A structured representation of a plan"
    step_id: int
    description: str
    # eventuall wil have more info such as assigned agent and status, result