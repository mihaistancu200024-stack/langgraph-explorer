from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END
from anthropic import Anthropic
import os

METADATA = {
    "id": "graph6",
    "name": "LLM Node via Claude",
    "description": "Passes a prompt to Claude (claude-sonnet-4-6) and returns the response.",
    "input_schema": {
        "prompt": "string",
    },
}


class LLMState(TypedDict):
    prompt: str
    response: NotRequired[str]


def llm_node(state: LLMState) -> dict:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": state["prompt"]}],
    )
    return {"response": response.content[0].text}


def build_graph():
    builder = StateGraph(LLMState)
    builder.add_node("llm_node", llm_node)
    builder.add_edge(START, "llm_node")
    builder.add_edge("llm_node", END)
    return builder.compile()


def get_mermaid() -> str:
    return build_graph().get_graph().draw_mermaid()
