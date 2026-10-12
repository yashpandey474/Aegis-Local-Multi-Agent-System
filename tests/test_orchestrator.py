from unittest.mock import Mock

from main.agents.analyst import AnalystAgent
from main.llm.ollama import LLMResponse
from main.orchestration.orchestrator import Orchestrator
from main.planning.models import Plan, PlanStep


def test_orchestrator_executes_plan_sequentially():
    planner = Mock()
    analyst = Mock(spec=AnalystAgent)

    planner.create_plan.return_value = Plan(
        task="Calculate CAGR.",
        steps=(
            PlanStep(1, "Calculate CAGR."),
            PlanStep(2, "Compare CAGR with 10%."),
        ),
    )

    analyst.run.side_effect = [
        LLMResponse(content="12.47%", model="test"),
        LLMResponse(content="12.47% exceeds 10%.", model="test"),
    ]

    orchestrator = Orchestrator(
        planner=planner,
        analyst=analyst,
    )

    state = orchestrator.execute(
        "Calculate whether CAGR exceeds 10%."
    )

    assert state.success
    assert len(state.results) == 2
    assert state.results[0].output == "12.47%"
    assert state.results[1].output == "12.47% exceeds 10%."

    assert analyst.run.call_count == 2


def test_orchestrator_stops_on_failure():
    planner = Mock()
    analyst = Mock(spec=AnalystAgent)

    planner.create_plan.return_value = Plan(
        task="Test failure.",
        steps=(
            PlanStep(1, "First step."),
            PlanStep(2, "Second step."),
        ),
    )

    analyst.run.side_effect = RuntimeError("Agent failed")

    orchestrator = Orchestrator(
        planner=planner,
        analyst=analyst,
    )

    state = orchestrator.execute("Test failure.")

    assert not state.success
    assert len(state.results) == 1
    assert not state.results[0].success
    assert "Agent failed" in state.results[0].error