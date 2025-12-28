from langgraph.graph import StateGraph, END
from graph.state import AgentState
from app.agents.planner import planner_node
from app.agents.websearch import websearch_node
from app.agents.rag import rag_node
from app.agents.evidence import evidence_node
from app.agents.summarizer import summarizer_node
from app.agents.degraded import degraded_summarizer_node
from app.agents.failure import failure_node
from app.routers.router import planner_router,evaluator_router
from app.agents.direct import direct_answer_node


graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("rag", rag_node)
graph.add_node("web_search", websearch_node)
graph.add_node("evidence_checker", evidence_node)
graph.add_node("direct_answer", direct_answer_node)
graph.add("degraded_summarizer",degraded_summarizer_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("failure_node", failure_node)

graph.set_entry_point("planner")

graph.add_conditional_edges(
    "planner",
    planner_router,
    {
        "direct": "direct_answer",
        "rag": "rag",
        "web": "web_search",
        "both": ["rag", "web_search"],
        "fail": "failure_node"
    }
)


graph.add_edge("rag", "evidence_checker")
graph.add_edge("web_search", "evidence_checker")

graph.add_conditional_edges(
    "evidence_checker",
    evaluator_router,
    {"retry_rag":"rag",
     "retry_web":"web",
     "retry_both":["rag","web_search"],
     "degrade_answer":"degraded_summarizer",
     "summarize":"summarizer",
     "fail":"failure_node"
     }
    )

graph.add_edge("degraded_summarizer",END)
graph.add_edge("summarizer", END)
graph.add_edge("failure_node", END)
