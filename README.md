# LangGraph Explorer

A full-stack portfolio project exploring [LangGraph](https://github.com/langchain-ai/langgraph) — a framework for building stateful, graph-based AI workflows. Includes a FastAPI backend exposing 8 progressively complex graphs and a React + Fluent UI frontend to invoke them, inspect results, and visualize graph structure.

![Stack](https://img.shields.io/badge/Python-3.10+-blue) ![Stack](https://img.shields.io/badge/FastAPI-backend-green) ![Stack](https://img.shields.io/badge/React-18-61dafb) ![Stack](https://img.shields.io/badge/Fluent_UI-v9-0078d4)

---

## Architecture

```
langgraph/
├── main.py          # Python foundations (standalone — see below)
├── graph1–4/        # Original standalone graph scripts
├── backend/         # FastAPI server + all 8 LangGraph graph modules
└── frontend/        # React + Fluent UI app
```

The frontend fetches graph metadata, renders a dynamic input form per graph, invokes the backend, and displays the result alongside a live Mermaid diagram of the graph structure.

---

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env       # add your ANTHROPIC_API_KEY (required for graph6)
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:3000`.

---

## Graphs

### Graph 1 — Greeting + Compliment
Single node. Demonstrates basic `StateGraph` setup, typed state, and injecting external data into nodes via closures.

### Graph 2 — Sum / Product
Multi-input state with `List[int]`, `str`, and `NotRequired[str]`. Shows how a node can perform conditional logic (sum vs product) using Python's `match` statement.

### Graph 3 — Sequential User Profile
Three nodes chained with explicit `add_edge`: `greet` → `add_age` → `add_skills`. State is built up incrementally across nodes.

### Graph 4 — Conditional Math Router
Two-stage conditional routing via `add_conditional_edges`. First router dispatches to `+`, `-`, or `*` nodes. Second router branches on even/odd result to apply `sqrt` or `power_2`. Demonstrates complex branching graphs.

### Graph 5 — Parallel Branches ⭐
Fan-out from `START` to two nodes that run simultaneously. Uses `Annotated[list, operator.add]` as a state reducer to safely merge parallel outputs. Demonstrates LangGraph's native parallel execution model.

### Graph 6 — LLM Node (Claude) ⭐
A node that calls `claude-sonnet-4-6` via the Anthropic SDK. Demonstrates integrating an LLM as a first-class graph node — the foundation for all agent-based graphs.

### Graph 7 — Memory / Persistence ⭐
Uses `MemorySaver` checkpointer. Each invocation with the same `thread_id` accumulates history across calls. Demonstrates stateful graphs that remember context between interactions.

### Graph 8 — Human-in-the-Loop ⭐
Compiled with `interrupt_before=["execute"]` and `MemorySaver`. The graph pauses after `prepare` and resumes only after the user approves — demonstrated live in the UI with Approve/Reject buttons.

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/graphs` | List all graphs with metadata and input schemas |
| `GET` | `/api/graphs/{id}/diagram` | Mermaid diagram string for a graph |
| `POST` | `/api/graphs/{id}/invoke` | Run a graph with input |
| `POST` | `/api/graphs/{id}/resume` | Resume a paused HITL graph |

---

## Python Foundations (`main.py`)

Standalone script covering:
- Type annotations: `TypedDict`, `Union`, `Optional`, `Any`, `NotRequired`
- Functional programming: `map`, `filter`, `reduce`, `zip`
- Lambdas, closures, first-class functions
- `match` / `case` pattern matching

---

## Requirements

- Python 3.10+ (`match`/`case` syntax)
- Node.js 18+
- Anthropic API key (graph 6 only)
