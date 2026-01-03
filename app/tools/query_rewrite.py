from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from app.llm.model import get_model

RewriteReason = Literal["retry_rag", "retry_web", "retry_both"]


def _basic_intent_guard(original: str, rewritten: str) -> bool:
    original_tokens = set(original.lower().split())
    rewritten_tokens = set(rewritten.lower().split())

    overlap = original_tokens & rewritten_tokens
    return len(overlap) / max(len(original_tokens), 1) >= 0.6


def rewrite_query(
    original_query: str,
    retry_stage: int,
    retry_reason: RewriteReason,
) -> str:
    """
    Rewrite a query to improve retrieval WITHOUT changing intent.
    """

    # HARD STOP — no infinite rewriting
    if retry_stage >= 3:
        return original_query

    if retry_reason == "retry_web":
        direction = "emphasize recent developments or updates"
    elif retry_reason == "retry_rag":
        direction = "clarify background or technical wording"
    else:
        direction = "broaden slightly to include overview and context"

    system_prompt = (
        "You are a query rewriter for an information retrieval system.\n"
        "Your job is to rewrite the query ONLY to improve search results.\n"
        "You must preserve the original intent, scope, and meaning EXACTLY.\n\n"
        "STRICT RULES:\n"
        "- Do NOT answer the question\n"
        "- Do NOT add new topics or entities\n"
        "- Do NOT remove existing constraints\n"
        "- Do NOT add opinions or conclusions\n"
        "- Keep the rewrite neutral and concise\n"
        "- Output ONLY the rewritten query\n"
    )

    user_prompt = (
        f"Original query:\n{original_query}\n\n"
        f"Rewrite goal:\n{direction}\n\n"
        f"Rewrite the query accordingly."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
    )

    llm = get_model()
    chain = prompt | llm

    response = chain.invoke({})  # IMPORTANT

    rewritten = response.content.strip()

    # Sanitize common LLM junk
    rewritten = rewritten.strip('"').strip("'").strip()

    if not rewritten:
        return original_query

    if not _basic_intent_guard(original_query, rewritten):
        return original_query

    return rewritten
