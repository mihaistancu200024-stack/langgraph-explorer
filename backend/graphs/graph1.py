from typing import TypedDict
from langgraph.graph import StateGraph, START, END

METADATA = {
    "id": "graph1",
    "name": "Greeting + Compliment",
    "description": "Combines a name and compliment into a personalized greeting message.",
    "input_schema": {
        "name": "string",
        "compliment": "string",
    },
}


class GreetingState(TypedDict):
    name: str
    compliment: str
    message: str


def personalize(state: GreetingState) -> dict:
    return {"message": f"{state['name']}, {state['compliment']}"}


def build_graph():
    builder = StateGraph(GreetingState)
    builder.add_node("personalize", personalize)
    builder.add_edge(START, "personalize")
    builder.add_edge("personalize", END)
    return builder.compile()


def get_mermaid() -> str:
    return build_graph().get_graph().draw_mermaid()
