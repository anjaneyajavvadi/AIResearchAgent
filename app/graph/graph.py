from langgraph.graph import StateGraph, END
from app.graph.state import AgentState

from app.agents.planner import planner_node
from app.agents.rag import rag_node
from app.agents.websearch import websearch_node
from app.agents.merger import merge_node
from app.agents.evidence import evidence_node
from app.agents.reducer import reducer_node
from app.agents.summarizer import summarizer_node
from app.agents.degraded import degraded_summarizer_node
from app.agents.failure import failure_node
from app.agents.direct import direct_answer_node
from app.routers.router import planner_router
from app.agents.evaluator_node import evaluator_node


def both_retrieval_node(state: AgentState):
    return state


graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("rag", rag_node)
graph.add_node("web_search", websearch_node)
graph.add_node("both_retrieval", both_retrieval_node)
graph.add_node("merge", merge_node)
graph.add_node("evidence_checker", evidence_node)
graph.add_node("evaluator", evaluator_node)
graph.add_node("reducer", reducer_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("degraded_summarizer", degraded_summarizer_node)
graph.add_node("failure_node", failure_node)
graph.add_node("direct_answer", direct_answer_node)

graph.set_entry_point("planner")

graph.add_conditional_edges(
    "planner",
    planner_router,
    {
        "direct": "direct_answer",
        "rag": "rag",
        "web": "web_search",
        "both": "both_retrieval",
        "fail": "failure_node",
    }
)

graph.add_edge("both_retrieval", "rag")
graph.add_edge("both_retrieval", "web_search")

graph.add_edge("rag", "merge")
graph.add_edge("web_search", "merge")



graph.add_edge("merge","evidence_checker")

graph.add_edge("evidence_checker", "evaluator")
graph.add_edge("evaluator", "reducer")

graph.add_conditional_edges(
    "reducer",
    lambda s: s["next_action"],
    {
        "retry_rag": "rag",
        "retry_web": "web_search",
        "retry_both": "both_retrieval",
        "summarize": "summarizer",
        "degrade_answer": "degraded_summarizer",
        "fail": "failure_node",
    }
)

graph.add_edge("summarizer", END)
graph.add_edge("degraded_summarizer", END)
graph.add_edge("failure_node", END)
graph.add_edge("direct_answer", END)
