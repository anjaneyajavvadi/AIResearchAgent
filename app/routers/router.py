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


def evaluator_router(state:AgentState):
    print("EVALUATOR ROUTER HIT")
    score=state['evidence_score']
    retries=state['retries']
    max_retries=state['max_retries']

    if (retries['rag']>=max_retries['rag'] and
        retries['web_search']>=max_retries['web_search']):
        if score.coverage>=0.4:
            return "degrade_answer"
        return "fail"

    if score.freshness<0.5:
        if retries['web_search']<max_retries['web_search']:
            return "retry_web"
        
        if retries['rag']<max_retries['rag']:
            return "retry_rag"
        return "degrade_answer"
    
    if score.coverage<0.6:
        if(retries['rag']<max_retries['rag'] or 
           retries['web_search']<max_retries['web_search']):
            return "retry_both"
        return "degrade_answer"
    
    if score.consistency<0.6:
        return "degrade_answer"
    
    return "summarize"
