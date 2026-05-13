from typing import Annotated, NotRequired
import operator
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

METADATA = {
    "id": "graph5",
    "name": "Parallel Branches",
    "description": "Fans out to two parallel branches (uppercase and reverse), then merges the results.",
    "input_schema": {
        "input": "string",
    },
}


class ParallelState(TypedDict):
    input: str
    results: Annotated[list, operator.add]
    final: NotRequired[str]


def branch_upper(state: ParallelState) -> dict:
    return {"results": [f"UPPERCASE: {state['input'].upper()}"]}


def branch_reverse(state: ParallelState) -> dict:
    return {"results": [f"REVERSED: {state['input'][::-1]}"]}


def merge(state: ParallelState) -> dict:
    return {"final": " | ".join(state["results"])}


def build_graph():
    builder = StateGraph(ParallelState)
    builder.add_node("branch_upper", branch_upper)
    builder.add_node("branch_reverse", branch_reverse)
    builder.add_node("merge", merge)

    # Parallel fan-out from START
    builder.add_edge(START, "branch_upper")
    builder.add_edge(START, "branch_reverse")

    # Both branches converge on merge
    builder.add_edge("branch_upper", "merge")
    builder.add_edge("branch_reverse", "merge")
    builder.add_edge("merge", END)

    return builder.compile()


def get_mermaid() -> str:
    return build_graph().get_graph().draw_mermaid()
