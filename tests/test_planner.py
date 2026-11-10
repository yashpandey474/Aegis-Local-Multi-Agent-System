import pytest
from main.llm.ollama import LocalLLM
from main.planning.planner import Planner

def test_planner() -> None:
    llm = LocalLLM()

    planner = Planner(llm)

    plan = planner.create_plan(
        "Calculate the CAGR when revenue increased "
        "from $10 billion to $18 billion over 5 years "
        "and determine whether the CAGR exceeded 10%."
    )


    for step in plan:
        print(f"{step.step_id}. {step.description}")