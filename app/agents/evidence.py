from app.graph.state import AgentState
from app.tools.evidence_scorer import evidence_checker

def evidence_node(state: AgentState):
    print("Evidence checker")
    response = evidence_checker(
        query=state["user_query"],
        rag_results=state.get("rag_results", []),
        web_results=state.get("web_search_results", [])
    )

    return {
        "evidence_score": response,
    }
