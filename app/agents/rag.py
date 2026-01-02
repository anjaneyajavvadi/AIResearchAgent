from app.graph.state import AgentState
from app.tools.rag_retrieval import rag_retrieve

def rag_node(state: AgentState):
    results = rag_retrieve(state["user_query"])

    return {
        "rag_results": results,
        "rag_done": True,
        "rag_failed": len(results) == 0
    }
