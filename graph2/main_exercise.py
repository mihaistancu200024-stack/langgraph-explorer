import math
from typing import List, NotRequired, TypedDict

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    numbers: List[int]
    sign: str
    name: str
    result: NotRequired[str]


def process_operation(state: AgentState) -> AgentState:
    match state["sign"]:
        case "*":
            value = math.prod(state["numbers"])
        case "+":
            value = sum(state["numbers"])
        case _:
            raise ValueError("Sign is not allowed")

    state["result"] = f"Hi {state['name']}, your answer is {value}"
    return state


if __name__ == "__main__":
    graph = StateGraph(AgentState)
    graph.add_node("operation", process_operation)
    graph.set_entry_point("operation")
    graph.set_finish_point("operation")
    graph_compiled = graph.compile()

    answers = graph_compiled.invoke(
        {"numbers": [1, 2, 3, 4], "name": "Mihai", "sign": "*"}
    )
    print(answers["result"])
