from tools.rag_retrieval import rag_retrieve
from graph.state import AgentState

def rag_node(state:AgentState):
    results=rag_retrieve(state['user_query'])

    state['retries']['rag']+=1
    return {'rag_results':results,'retries':state['retries']}

