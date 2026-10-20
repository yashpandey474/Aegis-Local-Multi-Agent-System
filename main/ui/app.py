from datetime import datetime

import streamlit as st

from main.application import build_orchestrator
from main.llm.ollama import OllamaConfig

st.set_page_config(
    page_title="Aegis | Local Agent System",
    layout="wide"
)

@st.cache_resource(show_spinner=False)
def get_orchestrator():
    return build_orchestrator()

if "runs" not in st.session_state:
    st.session_state["runs"] = []

if "selected_run_index" not in st.session_state:
    st.session_state["selected_run_index"] = 0

with st.sidebar:
    st.title("Aegis")
    st.caption("Local multi-agent AI system")

    st.divider()
    st.subheader("Runtime")

    config = OllamaConfig()
    st.write(f"Model: {config.model}")
    st.write(f"Endpoint; {config.host}")
    st.caption("Inference is handled by local Ollama server")

    st.divider()
    st.subheader("Run history")

    if st.session_state["runs"]:
        selected_index = st.selectbox(
            "Select a previous run",
            options=list(range(len(st.session_state["runs"]))),
            format_func=lambda index: (
                f"{st.session_state['runs'][index]['timestamp']} · "
                f"{st.session_state['runs'][index]['task'][:35]}"
            ),
            key="selected_run_index"
        )

        if st.button("Clear run history", use_container_width=True):
            st.session_state["runs"] = []
            st.session_state["selected_run_index"] = 0
            st.rerun()
    else:
        st.caption("Your completed runs will appear here.")

# Main page
st.title("Aegis")
st.markdown(
    "Submit a task and inspect how the planner and agent execute it."
)

with st.form("task_form", clear_on_submit=True):
    task = st.text_area(
        "What should Aegis do?",
        placeholder=(
            "Calculate whether a company growing from $100M to "
            "$160M over 4 years exceeded a 10% CAGR threshold."
        ),
        height=120,
    )

    submitted = st.form_submit_button(
        "Run task",
        type="primary",
        use_container_width=True
    )

if submitted:
    if not task.strip():
        st.warning("Enter a task before running Aegis.")
    else:
        try:
            with st.spinner("Planning and executing your task..."):
                orchestrator = get_orchestrator()
                state = orchestrator.execute(task.strip())

            st.session_state["runs"].insert(
                0,
                {
                    "task": task.strip(),
                    "timestamp": datetime.now().astimezone().strftime(
                        "%H:%M:%S"
                    ),
                    "state": state,
                },
            )

            # Automatically select the newly completed run.
            st.session_state["selected_run_index"] = 0
        except Exception as exc:
            st.error(
                "Aegis could not complete the run. "
                f"Check that Ollama is running and inspect the error: {exc}"
            )

runs = st.session_state["runs"]

if not runs:
    st.info(
        "Submit a task to see its plan, execution results and final output"
    )
    st.stop()

## Display current results
selected_index = st.session_state["selected_run_index"]
selected_run = runs[selected_index]
state = selected_run["state"]

st.divider()
st.subheader("Execution overview")
st.caption(f"Task submitted at {selected_run['timestamp']}")
st.markdown(f"**Task:** {selected_run['task']}")

successful_steps = sum(result.success for result in state.results)

col1, col2, col3 = st.columns(3)
col1.metric("Planned steps", len(state.plan.steps))
col2.metric("Executed steps", len(state.results))
col3.metric("Successful steps", successful_steps)


overview_tab, plan_tab, steps_tab = st.tabs(
    ["Final output", "Plan", "Step-by-step execution"]
)


with overview_tab:
    if state.success:
        st.success("Execution completed.")
    else:
        st.warning(
            "Execution stopped after a failure. "
            "Inspect the step results for details."
        )

    if state.final_output is not None:
        st.markdown(state.final_output)
    else:
        st.caption("No final output was produced.")



with plan_tab:
    st.markdown("### Planner output")

    for step in state.plan.steps:
        st.markdown(f"**Step {step.step_id}.** {step.description}")


with steps_tab:
    st.markdown("### Execution trace")

    results_by_step = {
        result.step_id: result
        for result in state.results
    }

    for step in state.plan.steps:
        result = results_by_step.get(step.step_id)

        if result is None:
            label = f"Step {step.step_id} · Not executed"
        elif result.success:
            label = f"Step {step.step_id} · Success"
        else:
            label = f"Step {step.step_id} · Failed"

        with st.expander(label):
            st.write(step.description)

            if result is None:
                st.caption(
                    "This step was not reached during execution."
                )
            elif result.success:
                st.markdown("**Result**")
                st.markdown(str(result.output))
            else:
                st.error(result.error or "Unknown error")
                