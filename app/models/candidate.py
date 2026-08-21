from typing import List

from pydantic import BaseModel, Field


class Candidate(BaseModel):
    name: str
    email: str

    education: List[str] = Field(default_factory=list)

    skills: List[str] = Field(default_factory=list)

    experience: List[str] = Field(default_factory=list)

    projects: List[str] = Field(default_factory=list)

    achievements: List[str] = Field(default_factory=list)