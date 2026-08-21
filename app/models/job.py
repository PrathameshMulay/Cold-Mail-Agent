from typing import List, Optional

from pydantic import BaseModel, Field


class Job(BaseModel):
    title: str
    company: str
    location: Optional[str] = None

    description: str

    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)

    responsibilities: List[str] = Field(default_factory=list)
    qualifications: List[str] = Field(default_factory=list)

    keywords: List[str] = Field(default_factory=list)