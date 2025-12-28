from typing import List
from tavily import TavilyClient
import os
from datetime import datetime
from urllib.parse import urlparse
from app.models.websearch_model import WebRetrievalResult
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(os.environ.get("TAVILY_API_KEY"))

from datetime import datetime
from urllib.parse import urlparse

def web_search(query: str, k: int = 8) -> List[WebRetrievalResult]:
    response = tavily.search(query=query, max_results=k)

    results = []

    for r in response.get("results", []):
        domain = urlparse(r.get("url", "")).netloc

        results.append(
            WebRetrievalResult(
                source_id=domain,
                title=r.get("title", ""),
                content=r.get("content", ""),
                snippet=r.get("content", "")[:500],
                url=r.get("url"),
                published_at=r.get("published_date"),
                retrieved_at=datetime.utcnow().isoformat(),
                relevance_score=float(r.get("score", 0.5)),
            )
        )

    return results

if __name__=="__main__":
    results=web_search("Any new things about the transformer archietcture")
    print(results)