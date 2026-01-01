from app.graph.graph import graph
import atexit
from app.llm.qdrant import close_qdrant_client
app = graph.compile()

initial_state = {
    "user_query": "Tell me about the recent updates in the architercture of transformers",
    "rag_results": [],
    "web_search_results": [],
    "evidence_score": None,
    "retries": {
        "rag": 0,
        "web_search": 0,
        "synthesis": 0
    },
    "max_retries": {
        "rag": 2,
        "web_search": 2,
        "synthesis": 2
    },
    
}

result = app.invoke(initial_state)

print(result['final_response'])

atexit.register(close_qdrant_client)
