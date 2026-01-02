from typing import List
from datetime import date
from app.models.evidence_score_model import EvidenceScore
from app.models.rag_retrieval_model import RagRetrievalResult
from app.models.websearch_model import WebRetrievalResult

def evidence_checker(
    query: str,
    rag_results: List[RagRetrievalResult],
    web_results: List[WebRetrievalResult],
) -> EvidenceScore:

    all_results = rag_results + web_results

    source_ids = set()

    for r in rag_results:
        source_ids.add("arxiv")

    for w in web_results:
        if w.source_id:
            source_ids.add(w.source_id)
        else:
            source_ids.add("web")

    source_diversity = len(source_ids)

    # ---------- FRESHNESS ----------
    current_year =date.today().year
    freshness_scores = []

    for r in rag_results:
        if r.year:
            age = current_year - r.year
            if age <= 2:
                freshness_scores.append(1.0)
            elif age <= 4:
                freshness_scores.append(0.6)
            else:
                freshness_scores.append(0.4)

    for w in web_results:
        if w.published_at:
            freshness_scores.append(0.8)  # assume recent unless proven old

    freshness = sum(freshness_scores) / len(freshness_scores) if freshness_scores else 0.0

    # ---------- COVERAGE ----------
    # simple heuristic first (LLM refinement can come later)
    coverage = min(1.0, len(all_results) / 6.0)

    # ---------- CONSISTENCY ----------
    # conservative default
    if len(all_results) <= 1:
        consistency = 0.4
    else:
        consistency = min(1.0, 0.5 + 0.1 * len(all_results))

    # ---------- USABLE ----------
    usable = (
        coverage >= 0.6 and
        consistency >= 0.6 and
        freshness >= 0.5
    )

    return EvidenceScore(
        coverage=round(coverage, 2),
        consistency=round(consistency, 2),
        freshness=round(freshness, 2),
        source_diversity=source_diversity,
        usable=usable,
    )
