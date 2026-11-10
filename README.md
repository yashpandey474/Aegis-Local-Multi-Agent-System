# Aegis — Local Multi-Agent AI System

Aegis is a local-first, LLM-powered agent orchestration system designed to execute complex tasks through planning, specialized agents, tool integrations, and structured execution workflows.

Built around locally hosted LLMs, Aegis explores the architecture of production-oriented agentic systems, with an emphasis on explicit agent contracts, controlled execution, extensibility, observability, and reliable task orchestration.

The project is being developed incrementally, with the eventual goal of supporting independently operating agents through **Agent-to-Agent (A2A)** communication and standardized tool integrations through the **Model Context Protocol (MCP)**.

## Architecture

```text
                       User
                        |
                        v
                  Streamlit UI
                        |
                        v
                    Planner
                   (Local LLM)
                        |
                        v
                  Generated Plan
                        |
                        v
                  Plan Validator
                        |
                        v
                  Orchestrator
                        |
                        v
                  Agent Registry
                        |
              +---------+---------+
              |                   |
              v                   v
         Analyst Agent       Future Agents
              |
              v
         Tool Registry
              |
          +---+---+
          |       |
          v       v
      Calculator  String Length
          |
          v
       Tool Result
          |
          v
     LLM Follow-up
          |
          v
     Agent Result
          |
          v
    Execution State
          |
          v
       UI Output
```

All LLM inference currently runs through a locally hosted Ollama instance.

## Core Components

### 1. Planning

The Planner decomposes user requests into sequential execution steps using an LLM.

Each step specifies:
- A unique step identifier.
- A task description.
- The agent responsible for execution.

Plans are represented using structured data models and validated before execution.

### 2. Agent Architecture

Agents implement a common interface and return structured `AgentResult` objects.

The architecture separates individual model responses from agent-level execution results, allowing agents to combine multiple LLM calls, tool invocations, and other operations behind a consistent interface.

### 3. Agent Registry

The Agent Registry maintains a mapping of registered agent names to their implementations.

The Planner receives descriptions of available agents and proposes an agent for each execution step. The Orchestrator resolves these assignments against the registry before executing the plan.

This provides extensible, registry-based agent routing without allowing LLM-generated responses to instantiate arbitrary executable components.

### 4. Tool Integration

Agents access deterministic capabilities through a Tool Registry.

Currently implemented tools include:

- **Calculator:** Evaluates arithmetic expressions using an AST-based evaluator with an explicit operator allowlist.
- **String Length:** Returns the character count of a string.

Tool calls use structured JSON representations and are parsed before execution.

### 5. Orchestration and Execution State

The Orchestrator coordinates planning, agent resolution, sequential execution, context passing, and failure handling.

Each execution maintains an `ExecutionState` containing:

- Original user task and generated plan.
- Unique execution identifier.
- Execution status.
- Individual step results.
- Execution events and timestamps.
- Per-step and total execution latency.

The current execution policy is sequential and fail-fast.

### 6. Streamlit Interface

A Streamlit-based interface provides a way to interact with Aegis and inspect individual executions.

Current capabilities include task submission, execution history, generated plans, step-level results, and execution traces.

## Technology Stack

| Component           | Technology                             |
| ------------------- | -------------------------------------- |
| Language            | Python                                 |
| LLM inference       | Ollama                                 |
| Local LLM           | Qwen (configurable)                    |
| Agent orchestration | Custom Python implementation           |
| User interface      | Streamlit                              |
| Data models         | Python dataclasses                     |
| Tool integration    | Custom Tool Registry                   |
| Execution tracking  | Structured execution events and timing |

## Getting Started

### Prerequisites

- Python 3.12+
- [Ollama](https://ollama.com/)
- A locally available Ollama model

### 1. Clone the repository

```bash
git clone https://github.com/yashpandey474/Aegis-local-multi-agent-system.git

cd Aegis-local-multi-agent-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv

source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the configured Ollama model

For the default configuration:

```bash
ollama pull qwen3:4b
```

Ensure the Ollama service is running and accessible at:

```text
http://localhost:11434
```

### 5. Launch Aegis

```bash
python -m streamlit run ui/app.py
```

Open the local Streamlit URL printed in the terminal, typically:

```text
http://localhost:8501
```

## Example Task

Submit a task such as:

> Calculate whether a company growing from $100M to $160M over four years exceeded a 10% CAGR threshold.

Aegis generates a plan, validates the requested agent assignments, executes the steps, invokes tools when necessary, and presents the results alongside an execution trace.

## Design Principles

**Constrained autonomy**

LLMs propose plans and tool calls, while the application retains control over validation, capability resolution, and execution.

**Explicit contracts**

Agents, tools, plans, and execution results use defined interfaces and structured data models.

**Separation of concerns**

Planning, orchestration, agent reasoning, deterministic tool execution, and user interaction are independent components.

**Local-first inference**

LLM inference is performed locally through Ollama, enabling experimentation without depending on hosted inference APIs.

**Observable execution**

Execution state, step outcomes, events, and latency are tracked explicitly to support debugging and future performance evaluation.

## Development Roadmap

- [x] Local LLM integration through Ollama
- [x] Agent abstraction and Analyst Agent
- [x] Structured JSON tool calls
- [x] Tool Registry and deterministic tool execution
- [x] Multi-step task planning
- [x] Plan validation
- [x] Agent Registry and registry-based routing
- [x] Sequential orchestration and execution state
- [x] Basic execution events and latency tracking
- [x] Streamlit interaction interface
- [ ] Research Agent and evidence provenance
- [ ] Specialized multi-agent workflows
- [ ] Agent-to-Agent (A2A) communication
- [ ] Model Context Protocol (MCP) integrations
- [ ] Verification Agent and evidence-grounded validation
- [ ] Persistent execution state and checkpointing
- [ ] Retry policies, timeouts, and fault tolerance
- [ ] Evaluation framework and reproducible benchmarks
- [ ] OpenTelemetry-based tracing and metrics
- [ ] Production deployment and containerization

## Project Status

Aegis is under active development. Its current implementation provides the foundational planning, tool-use, agent registry, orchestration, and interaction layers. Specialized agents, distributed agent communication, and production evaluation infrastructure are planned extensions.

The architecture and implementation will evolve as these capabilities are introduced.