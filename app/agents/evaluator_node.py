from app.graph.state import AgentState
from app.routers.router import evaluator_router

def evaluator_node(state: AgentState):
    decision = evaluator_router(state)
    return {"next_action": decision}
