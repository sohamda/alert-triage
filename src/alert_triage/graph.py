"""A deterministic LangGraph that parses, classifies and routes one log line.

parse -> classify -> page   (critical)
                  -> record (everything else)
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from alert_triage.classify import classify
from alert_triage.parse import LogEvent, parse_log_line


class TriageState(TypedDict, total=False):
    line: str
    event: LogEvent
    severity: str
    action: str


def _parse(state: TriageState) -> TriageState:
    return {"event": parse_log_line(state["line"])}


def _classify(state: TriageState) -> TriageState:
    return {"severity": classify(state["event"])}


def _route(state: TriageState) -> str:
    return "page" if state["severity"] == "critical" else "record"


def _page(state: TriageState) -> TriageState:
    return {"action": f"page on-call for {state['event'].service}"}


def _record(state: TriageState) -> TriageState:
    return {"action": "record"}


def build_graph():
    graph = StateGraph(TriageState)
    graph.add_node("parse", _parse)
    graph.add_node("classify", _classify)
    graph.add_node("page", _page)
    graph.add_node("record", _record)
    graph.add_edge(START, "parse")
    graph.add_edge("parse", "classify")
    graph.add_conditional_edges("classify", _route, {"page": "page", "record": "record"})
    graph.add_edge("page", END)
    graph.add_edge("record", END)
    return graph.compile()


def triage(line: str) -> TriageState:
    """Run one log line through the graph and return the final state."""
    return build_graph().invoke({"line": line})
