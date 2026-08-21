from typing import Optional

from pydantic import BaseModel, Field


class Recruiter(BaseModel):
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None

    linkedin_url: Optional[str] = None
    source_url: Optional[str] = None

    confidence_score: float = 0.0


class RecruiterRanking(BaseModel):
    recruiter_name: str
    recruiter_title: Optional[str] = None
    recruiter_location: Optional[str] = None
    linkedin_url: Optional[str] = None

    is_recruiter: bool
    recruiter_score: float = Field(ge=0, le=100)

    location_score: float = Field(ge=0, le=100)

    overall_score: float = Field(ge=0, le=100)

    reasoning: str


class RecruiterEmail(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    email: Optional[str] = None

    confidence_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    verification_status: Optional[str] = None

    company: Optional[str] = None
    domain: Optional[str] = None

from typing import List, Optional

from pydantic import BaseModel


class RecruiterExtraction(BaseModel):
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: str


class RecruiterExtractionList(BaseModel):
    recruiters: List[RecruiterExtraction]