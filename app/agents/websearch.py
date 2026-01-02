from app.graph.state import AgentState
from app.tools.web_search import web_search

def websearch_node(state: AgentState):
    results = web_search(state["user_query"])

    return {
        "web_search_results": results,
        "web_done": True,
        "web_failed": len(results) == 0
    }
