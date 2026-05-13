from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import uuid
from dotenv import load_dotenv

load_dotenv()

from graphs import graph1, graph2, graph3, graph4, graph5, graph6, graph7, graph8

app = FastAPI(title="LangGraph Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GRAPHS = {
    "graph1": graph1,
    "graph2": graph2,
    "graph3": graph3,
    "graph4": graph4,
    "graph5": graph5,
    "graph6": graph6,
    "graph7": graph7,
    "graph8": graph8,
}

# Build all compiled apps once at startup
compiled_apps: dict[str, Any] = {
    gid: mod.build_graph() for gid, mod in GRAPHS.items()
}


@app.get("/api/graphs")
def list_graphs():
    """Return metadata for all available graphs."""
    return [mod.METADATA for mod in GRAPHS.values()]


@app.get("/api/graphs/{graph_id}/diagram")
def get_diagram(graph_id: str):
    """Return the Mermaid diagram string for a graph."""
    if graph_id not in GRAPHS:
        raise HTTPException(status_code=404, detail=f"Graph '{graph_id}' not found.")
    return {"mermaid": GRAPHS[graph_id].get_mermaid()}


@app.post("/api/graphs/{graph_id}/invoke")
def invoke_graph(graph_id: str, body: dict):
    """Invoke a graph with the given input. Returns result, paused state, and thread_id."""
    if graph_id not in GRAPHS:
        raise HTTPException(status_code=404, detail=f"Graph '{graph_id}' not found.")

    app_instance = compiled_apps[graph_id]
    thread_id = body.pop("thread_id", str(uuid.uuid4()))
    config = {"configurable": {"thread_id": thread_id}}

    result = app_instance.invoke(body, config=config)

    # Detect HITL pause
    state = app_instance.get_state(config)
    paused = bool(state.next)

    return {"result": result, "paused": paused, "thread_id": thread_id}


class ResumeBody(BaseModel):
    thread_id: str


@app.post("/api/graphs/{graph_id}/resume")
def resume_graph(graph_id: str, body: ResumeBody):
    """Resume a paused (human-in-the-loop) graph by its thread_id."""
    if graph_id not in GRAPHS:
        raise HTTPException(status_code=404, detail=f"Graph '{graph_id}' not found.")

    config = {"configurable": {"thread_id": body.thread_id}}
    result = compiled_apps[graph_id].invoke(None, config=config)
    return {"result": result}
