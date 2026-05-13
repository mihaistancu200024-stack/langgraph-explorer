from typing import TypedDict, List, NotRequired
from langgraph.graph import StateGraph, START, END

METADATA = {
    "id": "graph3",
    "name": "Sequential User Profile",
    "description": "Builds a user profile message step by step through three chained nodes.",
    "input_schema": {
        "name": "string",
        "age": "number",
        "skills": "list",
    },
}


class ProfileState(TypedDict):
    name: str
    age: int
    skills: List[str]
    final: NotRequired[str]


def greet(state: ProfileState) -> dict:
    return {"final": f"Hi {state['name']}!"}


def add_age(state: ProfileState) -> dict:
    age = int(state["age"])
    return {"final": state.get("final", "") + f" You are {age} years old."}


def add_skills(state: ProfileState) -> dict:
    raw = state["skills"]
    if isinstance(raw, str):
        skills = [s.strip() for s in raw.split(",") if s.strip()]
    else:
        skills = list(raw)
    return {"final": state.get("final", "") + f" Your skills: {', '.join(skills)}"}


def build_graph():
    builder = StateGraph(ProfileState)
    builder.add_node("greet", greet)
    builder.add_node("add_age", add_age)
    builder.add_node("add_skills", add_skills)
    builder.add_edge(START, "greet")
    builder.add_edge("greet", "add_age")
    builder.add_edge("add_age", "add_skills")
    builder.add_edge("add_skills", END)
    return builder.compile()


def get_mermaid() -> str:
    return build_graph().get_graph().draw_mermaid()
