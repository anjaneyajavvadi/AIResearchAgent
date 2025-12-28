from typing import Literal, Optional
from pydantic import BaseModel

class WebRetrievalResult(BaseModel):
    # provenance
    source_type: Literal["web"] = "web"
    source_id: Optional[str]  # domain: arxiv.org, github.com, medium.com

    # identity
    title: str
    url: str

    # content
    content: str
    snippet: Optional[str]

    # time
    published_at: Optional[str]  # ISO if available
    retrieved_at: Optional[str]  # when you fetched it

    # retrieval signal (NOT evidence quality)
    relevance_score: float
