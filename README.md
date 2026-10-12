Planner -> What needs to be done?
Agent -> How should a particular task be done?
Tool -> Perform a concrete operation.

Example:
"Calculate the CAGR of a company's revenue and determine whether it exceeded 10%."

Planner:
1. Calculate CAGR from the revenue figures
2. Compare CAGR against 10%
3. Explain the result



Planner != Orchestrator
Planner:
Decides what should be done

Orchestrator:
Decides how the system actually executes that work

Planner -> decision about workflow
Orchestrator -> workflow execution engine
Agent -> reasoning/execution unit
Tool -> deterministic capability

LLM should not directly control your application's execution semantics

Eg:
Planner does not get to decide:
- whether step 2 executes if step 1 fails
- how results are stored
- what context is passed
- whether a step is retried
- how failures are represented
- what the final output is

- Constrained automony: the model supplies decisions within a system whose execution rules remain deterministic


Component	    Responsibility
Planner	        Decide the steps
Plan Validator	Enforce structural constraints
Orchestrator	Execute the workflow
Agent	        Perform reasoning
Tool Registry	Resolve capabilities
Tool	        Perform deterministic work
Execution State	Preserve workflow state