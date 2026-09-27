from main.planning.models import Plan

class PlanValidator:
    """
    LLM-generated plans are proposals, not commands.
    LLM Output -> validation -> application action
    """
    MAX_STEPS = 10

    @classmethod # has access to and can modify class-level data
    def validate(cls, plan: Plan) -> None:
        if not plan.task.strip():
            raise ValueError("Plan task cannot be empty.")

        if not plan.steps:
            raise ValueError("Plan must contain at least one step.")

        if len(plan.steps) > cls.MAX_STEPS:
            raise ValueError(
                f"Plan cannot contain more than {cls.MAX_STEPS} steps."
            )

        # step ids are correct
        expected_ids = range(1, len(plan.steps) + 1)
        actual_ids = [step.step_id for step in plan.steps]

        if actual_ids != list(expected_ids):
            raise ValueError(
                "Plan step IDs must be sequential starting from 1."
            )

        for step in plan.steps:
            # every step has a description
            if not step.description.strip():
                raise ValueError(
                            f"Step {step.step_id} has an empty description."
                        )
        

