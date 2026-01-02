from app.graph.state import AgentState

def planner_router(state: AgentState) -> str:
    answer_mode = state["answer_mode"]
    retrieval_mode = state["retrieval_mode"]

    if answer_mode == "refuse":
        return "fail"

    if answer_mode == "direct":
        return "direct"

    if retrieval_mode == "rag":
        return "rag"
    if retrieval_mode == "web":
        return "web"
    if retrieval_mode == "both":
        return "both"

    return "fail"


def evaluator_router(state: AgentState):
    score = state["evidence_score"]
    retries = state["retries"]
    max_retries = state["max_retries"]

    rag_exhausted = retries["rag"] >= max_retries["rag"]
    web_exhausted = retries["web_search"] >= max_retries["web_search"]

    # 1️⃣ Hard stop: nothing left to try
    if rag_exhausted and web_exhausted:
        if score.coverage >= 0.4:
            return "degrade_answer"
        return "fail"

    # 2️⃣ Freshness is bad → web helps most
    if score.freshness < 0.5:
        if not web_exhausted:
            return "retry_web"
        if not rag_exhausted:
            return "retry_rag"
        return "degrade_answer"

    # 3️⃣ Coverage is weak → need more sources
    if score.coverage < 0.6:
        if not rag_exhausted and not web_exhausted:
            return "retry_both"
        if not rag_exhausted:
            return "retry_rag"
        if not web_exhausted:
            return "retry_web"
        return "degrade_answer"

    # 4️⃣ Consistency is weak → retries won’t help much
    if score.consistency < 0.6:
        return "degrade_answer"

    # 5️⃣ Everything looks good
    return "summarize"
