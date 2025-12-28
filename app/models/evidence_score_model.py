from pydantic import BaseModel
from typing import Literal

class EvidenceScore(BaseModel):
    coverage: float        
    consistency: float     
    freshness: float       
    source_diversity: int  
    usable: bool    