from typing import Literal, Optional
from pydantic import BaseModel

class WebRetrievalResult(BaseModel):
    source_type: Literal["web"] = "web"
    source_id: Optional[str]

    title: str
    url: str

    content: str
    snippet: Optional[str]

    published_at: Optional[str]
    retrieved_at: Optional[str]  

    relevance_score: float
