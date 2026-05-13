from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from numpy import sqrt


class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: int | float


def adder(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number1"] + state["number2"]
    return state


def subtractor(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number1"] - state["number2"]
    return state


def multiplier(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number1"] * state["number2"]
    return state


def decide_first_hop(state: AgentState) -> str:
    operation = state["operation"]
    match operation:
        case "+":
            return "addition_operation"
        case "-":
            return "subtraction_operation"
        case "*":
            return "multiply_operation"
        case _:
            raise ValueError("Not implemented")


def square_root(state: AgentState) -> AgentState:
    state["finalNumber"] = float(sqrt(state["finalNumber"])).__round__(2)
    return state


def power_2(state: AgentState) -> AgentState:
    state["finalNumber"] = state["finalNumber"] * state["finalNumber"]
    return state


def decide_second_hop(state: AgentState) -> str:
    final_number = state["finalNumber"]
    print(f"Final number is {final_number}")
    if final_number % 2 == 0:
        return "square_operation"

    return "power_2_operation"


if __name__ == "__main__":
    graph = StateGraph(AgentState)
    graph.add_node("add_node", adder)
    graph.add_node("subtract_node", subtractor)
    graph.add_node("multiply_node", multiplier)
    graph.add_node("square_root", square_root)
    graph.add_node("power_2", power_2)
    graph.add_node("router1", lambda state: state)  # passthhrough function
    graph.add_node("router2", lambda state: state)  # passthhrough function
    graph.add_edge(START, "router1")

    graph.add_conditional_edges(
        "router1",
        decide_first_hop,
        {
            "addition_operation": "add_node",
            "subtraction_operation": "subtract_node",
            "multiply_operation": "multiply_node",
        },
    )

    graph.add_edge("add_node", "router2")
    graph.add_edge("subtract_node", "router2")
    graph.add_edge("multiply_node", "router2")
    graph.add_conditional_edges(
        "router2",
        decide_second_hop,
        {"square_operation": "square_root", "power_2_operation": "power_2"},
    )
    graph.add_edge("square_root", END)
    graph.add_edge("power_2", END)
    app = graph.compile()
    png_bytes = app.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png_bytes)

    result = app.invoke({"number1": 3, "number2": 2, "operation": "*"})  # type: ignore
    print(result)
