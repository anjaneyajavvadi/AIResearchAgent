from app.graph.state import AgentState

def merge_node(state: AgentState):
    return {
        # Ensure both fields exist and are normalized
        "rag_results": state.get("rag_results", []),
        "web_search_results": state.get("web_search_results", []),
    }
