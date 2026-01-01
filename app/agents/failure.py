from app.graph.state import AgentState

def failure_node(state: AgentState):
    return {
        "final_response": (
            "I wasn’t able to find reliable evidence to answer this question. "
            "The available information was either insufficient or inconsistent."
        )
    }