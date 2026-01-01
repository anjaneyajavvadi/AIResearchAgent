import re
from typing import List
from app.models.rag_retrieval_model import RagRetrievalResult
from rank_bm25 import BM25Okapi
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import json
from app.llm.qdrant import get_qdrant_client,close_qdrant_client

ARXIV_YEAR_RE = re.compile(r"^(\d{2})")

COLLECTION = "arxiv_ai_research_papers" 
with open("data/bm25.json") as f: 
    data = json.load(f) 

bm25 = BM25Okapi(data["corpus"]) 
ids = data["ids"] 
client = get_qdrant_client()
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def parse_year_and_version(arxiv_id: str):
    """
    arxiv_id example: 2305.14858v2
    """
    version = None
    if "v" in arxiv_id:
        base, version = arxiv_id.split("v", 1)
    else:
        base = arxiv_id

    match = ARXIV_YEAR_RE.match(base)
    year = None
    if match:
        yy = int(match.group(1))
        year = 2000 + yy if yy < 90 else 1900 + yy

    return year, f"v{version}" if version else None


def rag_retrieve(query: str) -> List[RagRetrievalResult]:
    tokens = query.lower().split()

    bm25_scores = bm25.get_scores(tokens)
    bm25_top = sorted(
        zip(ids, bm25_scores),
        key=lambda x: x[1],
        reverse=True
    )[:30]

    bm25_map = {i: score for i, score in bm25_top}

    query_vector = embedder.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    dense = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=20,
        with_payload=True,
        with_vectors=False
    )
    

    

    results: List[RagRetrievalResult] = []

    for p in dense.points:
        payload = p.payload or {}
        arxiv_id = payload.get("arxiv_id")

        if not arxiv_id or arxiv_id not in bm25_map:
            continue

        bm25_score = bm25_map[arxiv_id]
        dense_score = p.score

        relevance_score = (
            0.6 * dense_score +
            0.4 * min(bm25_score / 10.0, 1.0)
        )

        year, version = parse_year_and_version(arxiv_id)

        results.append(
            RagRetrievalResult(
                arxiv_id=arxiv_id,
                title=payload.get("title", ""),
                abstract=payload.get("abstract"),
                text=payload.get("abstract"),  
                year=year,
                version=version,
                bm25_score=bm25_score,
                dense_score=dense_score,
                relevance_score=relevance_score,
                url=f"https://arxiv.org/abs/{arxiv_id}",
            )
        )

    results.sort(key=lambda r: r.relevance_score, reverse=True)
    return results
