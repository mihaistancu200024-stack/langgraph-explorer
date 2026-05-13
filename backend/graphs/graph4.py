from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END
import numpy

METADATA = {
    "id": "graph4",
    "name": "Conditional Math Router",
    "description": "Routes arithmetic operations (+, -, *) then applies a secondary transformation based on whether the result is even or odd.",
    "input_schema": {
        "number1": "number",
        "operation": "string",
        "number2": "number",
    },
}


class MathState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: NotRequired[float]


# ── Primary operation nodes ──────────────────────────────────────────────────

def add_node(state: MathState) -> dict:
    return {"finalNumber": int(state["number1"]) + int(state["number2"])}


def subtract_node(state: MathState) -> dict:
    return {"finalNumber": int(state["number1"]) - int(state["number2"])}


def multiply_node(state: MathState) -> dict:
    return {"finalNumber": int(state["number1"]) * int(state["number2"])}


# ── Secondary transformation nodes ──────────────────────────────────────────

def square_root(state: MathState) -> dict:
    val = float(state.get("finalNumber", 0))
    return {"finalNumber": round(float(numpy.sqrt(val)), 2)}


def power_2(state: MathState) -> dict:
    val = float(state.get("finalNumber", 0))
    return {"finalNumber": round(val ** 2, 2)}


# ── Router passthrough nodes ─────────────────────────────────────────────────

def router1(state: MathState) -> dict:
    return {}


def router2(state: MathState) -> dict:
    return {}


# ── Conditional edge functions ───────────────────────────────────────────────

def route_operation(state: MathState) -> str:
    op = str(state.get("operation", "+")).strip()
    if op == "-":
        return "subtract_node"
    if op == "*":
        return "multiply_node"
    return "add_node"


def route_parity(state: MathState) -> str:
    val = state.get("finalNumber", 0)
    try:
        if int(val) % 2 == 0:
            return "square_root"
    except (ValueError, TypeError):
        pass
    return "power_2"


def build_graph():
    builder = StateGraph(MathState)

    builder.add_node("router1", router1)
    builder.add_node("add_node", add_node)
    builder.add_node("subtract_node", subtract_node)
    builder.add_node("multiply_node", multiply_node)
    builder.add_node("router2", router2)
    builder.add_node("square_root", square_root)
    builder.add_node("power_2", power_2)

    builder.add_edge(START, "router1")
    builder.add_conditional_edges(
        "router1",
        route_operation,
        {"add_node": "add_node", "subtract_node": "subtract_node", "multiply_node": "multiply_node"},
    )
    builder.add_edge("add_node", "router2")
    builder.add_edge("subtract_node", "router2")
    builder.add_edge("multiply_node", "router2")
    builder.add_conditional_edges(
        "router2",
        route_parity,
        {"square_root": "square_root", "power_2": "power_2"},
    )
    builder.add_edge("square_root", END)
    builder.add_edge("power_2", END)

    return builder.compile()


def get_mermaid() -> str:
    return build_graph().get_graph().draw_mermaid()
