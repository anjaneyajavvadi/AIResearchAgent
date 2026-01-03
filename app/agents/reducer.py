from app.graph.state import AgentState
from app.tools.query_rewrite import rewrite_query

def reducer_node(state: AgentState):
    retries = dict(state["retries"])

    if state.get("rag_failed"):
        retries["rag"] += 1
    if state.get("web_failed"):
        retries["web_search"] += 1

    action = state["next_action"]
    retry_stage = max(retries["rag"], retries["web_search"])



    if action.startswith("retry") and retry_stage > 0:
        effective_query = rewrite_query(
            original_query=state["user_query"],
            retry_stage=retry_stage,
            retry_reason=action
        )

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
