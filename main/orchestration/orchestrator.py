from main.agents.analyst import AnalystAgent
from main.orchestration.models import ExecutionState, StepResult
from main.planning.planner import Planner

class Orchestrator:
    def __init__(self, planner: Planner, analyst: AnalystAgent) -> None:
        self.planner = planner
        self.analyst = analyst

    def execute(self, task: str) -> ExecutionState:
        plan = self.planner.create_plan(task)
        state = ExecutionState(task=task, plan=plan)

        for step in plan.steps:
            step_task = self._build_step_context(state, step.description)

            try:
                # all steps go to analyst agent
                # that has a set of rules that it can run
                response = self.analyst.run(step_task)

                state.results.append(
                    StepResult(
                        step_id=step.step_id,
                        success=True,
                        output=response.content,
                    )
                )
            except Exception as exc:
                """
                Failure handling has to improve and be intelligent
                The plan could have been wrong, the agent being used could be wrong
                An agentic system is not just about successful execution, it is about behaviour under failure.
                """
                state.results.append(
                    StepResult(
                        step_id=step.step_id,
                        success=False,
                        error=str(exc)
                    )
                )

                # stop execution if one step errored out, sequential orchestration
                break
        
        return state

    @staticmethod
    def _build_step_context(
        state: ExecutionState,
        current_step: str, # description of step
    ) -> str:
        """
        The orchestrator performs context assembly.
        We want to trim down the previous step results passed to LLM to only the relevant ones for this step.
        And maybe pass on the tool outputs used previously for reuse (or should it be cached at tooling layer?)
        """
        previous_results = []

        for result in state.results:
            if result.success:
                # context passed to LLM contains results of previous steps
                # since it is sequential, all previous steps were successful
                previous_results.append(
                    f"Step {result.step_id} result:\n{result.output}"
                )
            else:
                # we don't hit this path currently
                previous_results.append(
                    f"Step {result.step_id} failed:\n{result.error}"
                )
        context = "\n\n".join(previous_results)

        return f"""
            ### Original task:
            {state.task}

            ### Current step;
            {current_step}

            ### Previous step results:
            {context if context else "None"}
        """
