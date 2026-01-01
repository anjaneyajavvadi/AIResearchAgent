from app.graph.state import AgentState
from app.tools.web_search import web_search

def websearch_node(state: AgentState):
    print(">>> ENTERED websearch_node, QUERY =", state.get("user_query"))
    results = web_search(state["user_query"])
    print(">>> WEB RESULTS COUNT =", len(results))

    retries=dict(state.get("retries",{}))
    retries['web_search']=retries.get('web_search',0)+1

    return {"web_search_results": results,'web_done':True,'retries':retries}

