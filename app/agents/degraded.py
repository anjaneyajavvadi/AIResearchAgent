from app.llm.model import get_model
from app.graph.state import AgentState

DEGRADED_SUMMARIZER_PROMPT = """
You are a research assistant producing a cautious, partial answer.

Rules (STRICT – DO NOT VIOLATE):
- Use ONLY the provided evidence.
- Do NOT assume the evidence is complete or comprehensive.
- Explicitly state limitations, uncertainty, or gaps.
- Do NOT generalize or extrapolate beyond the evidence.
- Avoid strong claims (no "clearly", "definitively", "proves", "state-of-the-art").
- Prefer observations and reported findings over conclusions.
- If evidence is insufficient to answer the question fully, say so clearly.

The goal is honesty and precision, not completeness.
"""

def degraded_summarizer_node(state: AgentState):
    llm = get_model()

    rag_results = state.get("rag_results", [])
    web_results = state.get("web_search_results", [])
    query = state["user_query"]
    score = state.get("evidence_score")

    evidence_ = []

    for r in rag_results:
        evidence_.append(
            f"[RAG | arXiv:{r.arxiv_id}]\n"
            f"Title: {r.title}\n"
            f"Abstract: {r.abstract}\n"
        )

    for w in web_results:
        evidence_.append(
            f"[WEB | {w.source_id or 'unknown'}]\n"
            f"Title: {w.title}\n"
            f"Content: {w.content}\n"
        )

    evidence_text = "\n\n".join(evidence_)

    prompt = f"""
{DEGRADED_SUMMARIZER_PROMPT}

User Query:
{query}

Evidence Quality Signals:
- Coverage: {score.coverage if score else "unknown"}
- Consistency: {score.consistency if score else "unknown"}
- Freshness: {score.freshness if score else "unknown"}

Evidence:
{evidence_text}
"""

    response = llm.invoke(prompt)

    return {
        "final_response": response
    }
