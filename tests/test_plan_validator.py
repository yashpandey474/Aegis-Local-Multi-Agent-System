import pytest

from main.planning.models import Plan, PlanStep
from main.planning.validator import PlanValidator


def test_valid_plan():
    plan = Plan(
        task="Calculate CAGR.",
        steps=(
            PlanStep(1, "Calculate CAGR."),
            PlanStep(2, "Compare CAGR with 10%."),
        ),
    )

    PlanValidator.validate(plan)


def test_empty_plan():
    plan = Plan(
        task="Calculate CAGR.",
        steps=(),
    )

    with pytest.raises(ValueError):
        PlanValidator.validate(plan)


def test_too_many_steps():
    plan = Plan(
        task="Calculate CAGR.",
        steps=tuple(
            PlanStep(i, f"Step {i}")
            for i in range(1, 12)
        ),
    )

    with pytest.raises(ValueError):
        PlanValidator.validate(plan)


def test_invalid_step_ids():
    plan = Plan(
        task="Calculate CAGR.",
        steps=(
            PlanStep(1, "Calculate CAGR."),
            PlanStep(3, "Compare CAGR."),
        ),
    )

    with pytest.raises(ValueError):
        PlanValidator.validate(plan)