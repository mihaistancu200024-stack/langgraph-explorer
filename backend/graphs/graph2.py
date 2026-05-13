from typing import TypedDict, List, NotRequired
from langgraph.graph import StateGraph, START, END

METADATA = {
    "id": "graph2",
    "name": "Sum / Product",
    "description": "Sums a list of numbers and formats the result with a label name.",
    "input_schema": {
        "values": "list",
        "name": "string",
    },
}


class SumState(TypedDict):
    values: List[int]
    name: str
    result: NotRequired[str]


def process(state: SumState) -> dict:
    raw = state["values"]
    # Accept comma-separated string or already a list
    if isinstance(raw, str):
        numbers = [int(v.strip()) for v in raw.split(",") if v.strip()]
    else:
        numbers = [int(v) for v in raw]
    total = sum(numbers)
    return {"result": f"{state['name']}: sum of {numbers} = {total}"}


def build_graph():
    builder = StateGraph(SumState)
    builder.add_node("process", process)
    builder.add_edge(START, "process")
    builder.add_edge("process", END)
    return builder.compile()


def get_mermaid() -> str:
    return build_graph().get_graph().draw_mermaid()
