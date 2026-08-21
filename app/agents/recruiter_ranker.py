from typing import List

from app.models.recruiter import Recruiter
from app.models.recruiter import RecruiterRanking
from app.services.llm import get_llm


class RecruiterRanker:

    def __init__(self):
        self.llm = get_llm()

    def rank(
        self,
        job,
        recruiters: List[Recruiter],
    ) -> List[Recruiter]:

        if not recruiters:
            return []

        structured_llm = self.llm.with_structured_output(
            RecruiterRanking
        )

        ranked = []

        for recruiter in recruiters:

            prompt = f"""
You are ranking people who may be recruiters for a job.

JOB
---
Title: {job.title}
Company: {job.company}
Location: {job.location}

RECRUITER
---------
Name: {recruiter.name}
Title: {recruiter.title}
Company: {recruiter.company}
Location: {recruiter.location}
LinkedIn: {recruiter.linkedin_url}


PRIORITY 1 — RECRUITER VALIDATION

Determine whether this person is actually involved in:

- Recruiting
- Talent acquisition
- Hiring
- Recruiting management

Examples generally considered recruiters:

- Recruiter
- Technical Recruiter
- Senior Recruiter
- Talent Acquisition Specialist
- Talent Acquisition Partner
- University Recruiter
- Campus Recruiter
- Recruiting Manager
- Talent Partner

Examples generally NOT considered recruiters:

- Data Scientist
- Data Analyst
- Software Engineer
- Machine Learning Engineer
- Product Manager
- Business Analyst
- Consultant

Set is_recruiter to true only when the available information
supports that the person is actually involved in recruiting.

Recruiter score:

100 = clearly a recruiter / talent acquisition professional
75 = likely recruiting-related but not completely clear
50 = uncertain
25 = unlikely to be a recruiter
0 = clearly not a recruiter


PRIORITY 2 — LOCATION

Compare the recruiter's location with the job location.

Location score:

100 = exact same city
80 = same metropolitan area
60 = same state but different metro
30 = different state, same country
0 = unknown or clearly outside the country

Do not invent a location.

Recruiter status is more important than location.


OVERALL SCORE

If is_recruiter is TRUE:

overall_score = 50 + (location_score * 0.50)

If is_recruiter is FALSE:

overall_score = location_score * 0.50


REASONING

Provide concise reasoning explaining:

1. Why the person is or is not a recruiter.
2. How their location compares with the job location.
"""

            ranking = structured_llm.invoke(prompt)

            ranked.append(
                (
                    recruiter,
                    ranking.overall_score,
                )
            )

        # Sort the ORIGINAL Recruiter objects
        # using the scores produced by the LLM.
        ranked.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            recruiter
            for recruiter, score in ranked
        ]
    
    