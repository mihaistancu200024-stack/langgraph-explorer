from typing import Optional, TypedDict

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    age: int
    final: str


def first_node(state: AgentState) -> AgentState:
    """This is the first node of our sequence"""
    state["final"] = f"Hi {state['name']}"
    return state


def second_node(state: AgentState) -> AgentState:
    """This is the second node of our sequence"""
    state["final"] = state["final"] + f", you are {state['age']} years old!"
    return state


if __name__ == "__main__":
    graph = StateGraph(AgentState)
    graph.add_node("first_node", first_node)
    graph.add_node("second_node", second_node)
    graph.set_entry_point("first_node")

    graph.add_edge("first_node", "second_node")
    graph.set_finish_point("second_node")

    app = graph.compile()
    state: AgentState = {"name": "Mihai", "age": 26}  # type: ignore

    png_bytes = app.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png_bytes)

    result = app.invoke(state)
    print(result)
