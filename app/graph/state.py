from typing import TypedDict,List,Dict,Optional,Literal
from app.models.rag_retrieval_model import RagRetrievalResult
from app.models.websearch_model import WebRetrievalResult
from app.models.evidence_score_model import EvidenceScore
import operator
from typing import Annotated

class RetryState(TypedDict):
    rag:Annotated[list,operator.add]
    web_search:Annotated[list,operator.add]
    synthesis:Annotated[list,operator.add]


class AgentState(TypedDict):
    user_query:str

    retrieval_mode:Literal['rag','web','both','none']
    answer_mode:Literal['grounded','direct','refuse']
    research_relevant:bool

    rag_results:Optional[List[RagRetrievalResult]]
    web_search_results:Optional[List[WebRetrievalResult]]

    rag_done:bool
    web_done:bool

    evidence_score:Optional[EvidenceScore]

    retries:RetryState
    max_retries:RetryState

    final_response:Optional[str]