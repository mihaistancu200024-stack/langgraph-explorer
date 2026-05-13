from typing import Any, Dict, TypedDict

from langgraph.graph import (
    StateGraph,  # framework that helps you design and manage the flow of tasks in your applications using a graph
)


def first_graph() -> StateGraph:
    # I now create an AgentState - shared data structure that keeps track of information as your application runs
    class AgentState(TypedDict):  # Our state schema
        """Defines the structure of the state that will be passed through the graph nodes"""

        message: str

    def greeting_node(state: AgentState) -> AgentState:
        """Simple node that adds a greeting message to the state"""

        state["message"] = "Hey " + state["message"] + ", how is your day going?"
        return state

    graph = StateGraph(AgentState)

    graph.add_node("greeter", greeting_node)

    graph.set_entry_point("greeter")
    graph.set_finish_point("greeter")
    return graph


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


def second_graph(person: Person) -> Any:
    class AgentState(TypedDict):
        compliment: str

    def personalize_compliment(state: AgentState) -> AgentState:
        state["compliment"] = f"{person.name}, {state['compliment']}"

        return state

    graph = StateGraph(AgentState)
    graph.add_node("personalizer", personalize_compliment)
    graph.set_entry_point("personalizer")
    graph.set_finish_point("personalizer")
    return graph


if __name__ == "__main__":
    person = Person(name="Bob", age=30)
    second_graph_compiled = second_graph(person).compile()
    second_graph_result = second_graph_compiled.invoke({"compliment": "amazing work!"})
    print(second_graph_result["compliment"])
