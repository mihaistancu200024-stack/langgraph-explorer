from typing import TypedDict

from langgraph.graph import StateGraph


class UserState(TypedDict):
    name: str
    age: int
    skills: list[str]
    final: str


def greet_user(state: UserState) -> UserState:
    state["final"] = f"Hi {state['name']}, hope you are well!"
    return state


def specify_user_age(state: UserState) -> UserState:
    state["final"] = state["final"] + f"you are {state['age']} years old"
    return state


def specify_user_skills(state: UserState) -> UserState:
    state["final"] = state["final"] + f"your skills are {', '.join(state['skills'])}"
    return state


if __name__ == "__main__":
    graph = StateGraph(UserState)
    graph.add_node("user_greeter", greet_user)
    graph.add_node("user_age", specify_user_age)
    graph.add_node("user_skills", specify_user_skills)
    graph.add_edge("user_greeter", "user_age")
    graph.add_edge("user_age", "user_skills")
    graph.set_entry_point("user_greeter")
    graph.set_finish_point("user_skills")
    app = graph.compile()

    png_bytes = app.get_graph().draw_mermaid_png()
    with open("graph2.png", "wb") as f:
        f.write(png_bytes)

    result = app.invoke({"name": "Mihai", "age": 26, "skills": ["dancing", "coding"]})  # type: ignore
    print(result["final"])
