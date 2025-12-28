from typing import Literal, Optional
from pydantic import BaseModel

class RagRetrievalResult(BaseModel):
    source_type: Literal["rag"] = "rag"
    source_id: Literal["arxiv"] = "arxiv"

    arxiv_id: str
    title: str
    url: str

    abstract: Optional[str]
    text: Optional[str]

    year: Optional[int]
    version: Optional[str]

    bm25_score: float
    dense_score: float
    relevance_score: float
