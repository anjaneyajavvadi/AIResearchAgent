from graph.state import AgentState
from tools.web_search import web_search

def websearch_node(state:AgentState):
    try:
        results=web_search(state['user_query'])
        state['retries']['web_search']+=1
        return {"websearch_results":results,'retries':state['retries']}

    except Exception as e:
        return {'failure_response':e}