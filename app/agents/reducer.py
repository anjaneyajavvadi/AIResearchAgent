from app.graph.state import AgentState

def reducer_node(state: AgentState):
    retries = dict(state["retries"])

    # update retries
    if state.get("rag_failed"):
        retries["rag"] += 1
    if state.get("web_failed"):
        retries["web_search"] += 1

    # update retrieval mode based on evaluator decision
    action = state["next_action"]

    if action == "retry_rag":
        retrieval_mode = "rag"
    elif action == "retry_web":
        retrieval_mode = "web"
    elif action == "retry_both":
        retrieval_mode = "both"
    else:
        retrieval_mode = state["retrieval_mode"]

    return {
        "retries": retries,
        "retrieval_mode": retrieval_mode
    }
