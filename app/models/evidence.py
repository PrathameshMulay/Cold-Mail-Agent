from typing import List

from pydantic import BaseModel, Field


class EvidenceMatch(BaseModel):
    capability: str
    evidence: str
    relevance_reason: str
    score: float = Field(ge=0, le=100)


class EvidenceSelection(BaseModel):
    matches: List[EvidenceMatch]