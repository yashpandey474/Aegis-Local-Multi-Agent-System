from time import perf_counter

from main.agents.analyst import AnalystAgent
from main.agents.registry import AgentRegistry
from main.agents.results import AgentResult
from main.orchestration.models import EventType, ExecutionEvent, ExecutionState, ExecutionStatus, StepResult, utc_now
from main.planning.planner import Planner

class Orchestrator:
    def __init__(self, planner: Planner, agent_registry: AgentRegistry) -> None:
        self.planner = planner
        self.agent_registry = agent_registry

    def execute(self, task: str) -> ExecutionState:

        # Latency tracking
        run_started_at = utc_now()
        run_clock = perf_counter()

        # Planning
        planning_clock = perf_counter()
        plan = self.planner.create_plan(
            task=task,
            available_agents=self.agent_registry.describe_agents()
        )
        
        planning_duration = perf_counter() - planning_clock

        # Plan created
        state = ExecutionState(task=task, plan=plan, started_at=run_started_at)

        # Track individual events for easier debugging
        # Started to execute plan
        state.events.append(
            ExecutionEvent(
                timestamp=run_started_at,
                event_type=EventType.EXECUTION_STARTED,
                message="Execution started."
            )
        )

        # We should probably have some validation here for the plan
        state.events.append(
            ExecutionEvent(
                timestamp=utc_now(),
                event_type=EventType.PLAN_CREATED,
                message="Plan generated and validated.",
                duration_seconds=planning_duration,
            )
        )

        # Step execution
        for step in plan.steps:
            # Latency tracking
            step_started_at = utc_now()
            step_clock = perf_counter()

            state.events.append(
                ExecutionEvent(
                    timestamp=step_started_at,
                    event_type=EventType.STEP_STARTED,
                    message=step.description,
                    step_id=step.step_id, # this step was started
                )
            )


            try:
                step_task = self._build_step_context(state, step.description)
                step_agent_name = step.agent_name

                agent_response: AgentResult = self.agent_registry.get(step_agent_name).run(step_task)

                finished_at = utc_now()
                duration = perf_counter() - step_clock

                state.results.append(
                    StepResult(
                        agent_name=agent_response.agent_name,
                        step_id=step.step_id,
                        success=True,
                        output=agent_response.output,
                        started_at=step_started_at,
                        finished_at = finished_at,
                        duration_seconds=duration
                    )
                )

                state.events.append(
                    ExecutionEvent(
                        timestamp=finished_at,
                        event_type=EventType.STEP_SUCCEEDED,
                        message="Step completed successfully.",
                        step_id=step.step_id,
                        duration_seconds=duration,
                    )
                )
            except Exception as exc:
                """
                Failure handling has to improve and be intelligent
                The plan could have been wrong, the agent being used could be wrong
                An agentic system is not just about successful execution, it is about behaviour under failure.
                """
                finished_at = utc_now()
                duration = perf_counter() - step_clock

                state.results.append(
                    StepResult(
                        agent_name=self.analyst.name
                        step_id=step.step_id,
                        success=False,
                        error=str(exc),
                        started_at=step_started_at,
                        finished_at=finished_at,
                        duration_seconds=duration,
                    )
                )

                state.events.append(
                    ExecutionEvent(
                        timestamp=finished_at,
                        event_type=EventType.STEP_FAILED,
                        message=str(exc),
                        step_id=step.step_id,
                        duration_seconds=duration,
                    )
                )

                self._finish(
                    state,
                    ExecutionStatus.FAILED,
                    run_clock
                )

                # stop execution if one step errored out, sequential orchestration
                return state

        self._finish(
            state,
            ExecutionStatus.SUCCEEDED,
            run_clock
        )        
        return state

    @staticmethod
    def _finish(
        state: ExecutionState,
        status: ExecutionStatus,
        run_clock: float,
    ) -> None:
        finished_at = utc_now()
        duration = perf_counter() - run_clock

        state.status = status
        state.finished_at = finished_at
        state.duration_seconds = duration


        event_type = (
            EventType.EXECUTION_SUCCEEDED
            if status == ExecutionStatus.SUCCEEDED
            else EventType.EXECUTION_FAILED
        )

        state.events.append(
            ExecutionEvent(
                timestamp=finished_at,
                event_type=event_type,
                message=f"Execution {status.value}.",
                duration_seconds=duration,
            )
        )
        
        
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
