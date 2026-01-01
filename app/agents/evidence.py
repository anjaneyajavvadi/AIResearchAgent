from app.graph.state import AgentState
from app.tools.evidence_scorer import evidence_checker

def evidence_node(state: AgentState):
    print("Evidence checker")
    response = evidence_checker(
        query=state["user_query"],
        rag_results=state.get("rag_results", []),
        web_results=state.get("web_search_results", [])
    )

    retries = dict(state["retries"])

    if response.coverage < 0.6:
        retries["rag"] += 1
        retries["web_search"] += 1

    return {
        "evidence_score": response,
        "retries": retries
    }
