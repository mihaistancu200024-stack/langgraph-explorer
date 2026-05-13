from typing import List, Optional, TypedDict

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    """Defines the structure of the state that will be passed through the graph nodes"""

    values: List[int]
    name: str
    result: Optional[str]


def process_values(state: AgentState) -> AgentState:
    state["result"] = f"Hi there {state['name']}! Your sum = {sum(state['values'])}"
    return state


graph = StateGraph(AgentState)
graph.add_node("processor", process_values)

if __name__ == "__main__":
    graph.set_entry_point("processor")
    graph.set_finish_point("processor")
    graph_compiled = graph.compile()

    png_bytes = graph_compiled.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png_bytes)
    answers = graph_compiled.invoke({"values": [1, 2, 3, 4], "name": "Steve"})  # type: ignore
    print(answers["result"])
