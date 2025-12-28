from typing import TypedDict,List,Dict,Optional,Literal
from app.models.rag_retrieval_model import RagRetrievalResult
from app.models.websearch_model import WebRetrievalResult
from app.models.evidence_score_model import EvidenceScore


class RetryState(TypedDict):
    rag:int
    web_search:int
    synthesis:int


class AgentState(TypedDict):
    user_query:str

    retrieval_mode:Literal['rag','web','both','none']
    answer_mode:Literal['grounded','direct','refuse']
    research_relevant:bool

    rag_results:Optional[List[RagRetrievalResult]]
    web_search_results:Optional[List[WebRetrievalResult]]

    evidence_score:Optional[EvidenceScore]

    retries:RetryState
    max_retries:RetryState

    final_response:Optional[str]