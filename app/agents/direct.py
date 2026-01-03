from app.graph.state import AgentState
from app.llm.model import get_model
from langchain_core.prompts import ChatPromptTemplate

DIRECT_ANSWER_PROMPT = """
You are answering a question using ONLY your general, time-invariant knowledge.

Rules (STRICT):
- Answer ONLY if the question can be answered without external or updated information.
- The answer must be stable over time and definitional in nature.
- Do NOT rely on research papers, benchmarks, trends, or comparisons.
- Do NOT speculate or extrapolate.
- Do NOT cite sources.
- If answering requires verification, recent information, or evidence, respond EXACTLY with:
  "This question requires external knowledge and cannot be answered directly."

Be concise and factual.
"""

def direct_answer_node(state: AgentState):
    llm = get_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", DIRECT_ANSWER_PROMPT),
        ("user", "{question}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "question": state["user_query"]
    })

    return {
        "final_response": response
    }
