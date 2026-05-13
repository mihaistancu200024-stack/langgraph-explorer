from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

METADATA = {
    "id": "graph8",
    "name": "Human-in-the-Loop",
    "description": "Prepares a task and pauses for human approval before executing it.",
    "input_schema": {
        "task": "string",
    },
}


class HITLState(TypedDict):
    task: str
    status: NotRequired[str]
    result: NotRequired[str]


def prepare(state: HITLState) -> dict:
    return {"status": f"Task prepared: {state['task']}. Awaiting approval."}


def execute(state: HITLState) -> dict:
    return {"result": f"Task '{state['task']}' executed successfully."}


def _build_base_graph():
    """Shared graph structure without checkpointer (used for diagram)."""
    builder = StateGraph(HITLState)
    builder.add_node("prepare", prepare)
    builder.add_node("execute", execute)
    builder.add_edge(START, "prepare")
    builder.add_edge("prepare", "execute")
    builder.add_edge("execute", END)
    return builder


def build_graph():
    return _build_base_graph().compile(
        checkpointer=MemorySaver(),
        interrupt_before=["execute"],
    )


def get_mermaid() -> str:
    return _build_base_graph().compile().get_graph().draw_mermaid()
