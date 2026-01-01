from app.tools.rag_retrieval import rag_retrieve
from app.graph.state import AgentState

def rag_node(state:AgentState):
    print(">>> ENTERED rag_node, QUERY =", state.get("user_query"))
    results=rag_retrieve(state['user_query'])
    
    retries=dict(state.get("retries",{}))
    retries['rag']=retries.get('rag',0)+1
    return {'rag_results':results,'rag_done':True,"retries":retries}

