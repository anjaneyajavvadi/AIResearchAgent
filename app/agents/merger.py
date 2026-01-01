from app.graph.state import AgentState

def merge_node(state: AgentState):
    print(">>> JOIN HIT")
    print("rag_done:", state.get("rag_done"))
    print("web_done:", state.get("web_done"))

    if not state.get("rag_done"):
        return {}   # not ready

    if not state.get("web_done"):
        return {}   # not ready

    # BOTH branches finished
    return {
        "rag_results": state["rag_results"],
        "web_search_results": state["web_search_results"]
    }
