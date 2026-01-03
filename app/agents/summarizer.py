from app.graph.state import AgentState
from app.llm.model import get_model

SUMMARIZER_PROMPT="""
You are a research assistant producing a grounded, evidence-based answer.

Rules (STRICT):
- Use ONLY the provided evidence.
- Do NOT introduce facts not present in the evidence.
- Synthesize information across multiple sources when possible.
- Resolve minor differences ONLY if evidence supports it.
- Be clear, structured, and technically precise.
- Avoid speculation and future predictions.
- If a detail is not supported by evidence, omit it.

Answer the user query based solely on the evidence below.
"""

def summarizer_node(state:AgentState):
    rag_results=state['rag_results']
    web_results=state['web_search_results']
    query=state['user_query']

    llm=get_model()

    evidence_=[]

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
{SUMMARIZER_PROMPT}

User Query:
{query}

Evidence:
{evidence_text}
"""
    response =llm.invoke(prompt)

    return {
        "final_response": response
    }

