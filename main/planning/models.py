from dataclasses import dataclass

@dataclass(frozen=True)
class PlanStep:
    "A structured representation of a plan"
    step_id: int
    description: str
    agent_name: str # the agent that will execute it, probably should be an Enum
    # eventuall wil have more info such as assigned agent and status, result


@dataclass(frozen=True)
class Plan:
    task: str
    steps: tuple[PlanStep, ...]