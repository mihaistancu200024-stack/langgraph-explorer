from typing import Annotated
import operator
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

METADATA = {
    "id": "graph7",
    "name": "Memory / Persistence",
    "description": "Accumulates messages across invocations using a MemorySaver checkpointer keyed by thread_id.",
    "input_schema": {
        "message": "string",
    },
}


class MemoryState(TypedDict):
    message: str
    history: Annotated[list, operator.add]


def remember(state: MemoryState) -> dict:
    return {"history": [state["message"]]}


def _build_base_graph():
    """Shared graph structure without checkpointer (used for diagram)."""
    builder = StateGraph(MemoryState)
    builder.add_node("remember", remember)
    builder.add_edge(START, "remember")
    builder.add_edge("remember", END)
    return builder


def build_graph():
    return _build_base_graph().compile(checkpointer=MemorySaver())


def get_mermaid() -> str:
    return _build_base_graph().compile().get_graph().draw_mermaid()
