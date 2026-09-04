from typing import List

from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.recruiter import RecruiterRanking
from app.services.llm import get_llm


class RecruiterRanker:

    def __init__(self):
        self.llm = get_llm()

    def rank(
        self,
        job: Job,
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
You are ranking recruiters for a job.

IMPORTANT:

The recruiter has ALREADY passed a hard company filter.

Therefore, DO NOT score or reconsider company association.

Your job is to rank recruiters primarily by LOCATION,
and secondarily by RECRUITER RELEVANCE.

==================================================
JOB
==================================================

Company:
{job.company}

Job Title:
{job.title}

Job Location:
{job.location}

Job Description:
{getattr(job, "description", "")}

==================================================
RECRUITER
==================================================

Name:
{recruiter.name}

Title:
{recruiter.title}

Company:
{recruiter.company}

Location:
{recruiter.location}

LinkedIn:
{recruiter.linkedin_url}

==================================================
PRIORITY 1 — LOCATION
==================================================

Location is the MOST IMPORTANT ranking factor.

Compare the recruiter's location with the job location.

Use:

100 = exact same city

80 = same metropolitan area

60 = same state

30 = different state, same country

0 = unknown location or outside the country

Do NOT invent a location.

A recruiter in the target city should generally
rank above a recruiter outside the target city.

==================================================
PRIORITY 2 — RECRUITER RELEVANCE
==================================================

Determine how relevant this recruiter appears
to the target job.

This is an ADDITIONAL ADVANTAGE, not a requirement.

Most recruiters do not publicly specify the
exact job functions they recruit for.

Therefore:

- Do NOT penalize a recruiter simply because
  their profile does not mention the target
  job function.
- Do NOT assume a recruiter is irrelevant
  because their specialization is unknown.
- General recruiters can still receive a high
  relevance score.
- Specific evidence of recruiting for the target
  function or job level is a bonus.

Examples of positive signals:

- Technical Recruiter
- Data/AI Recruiter
- Engineering Recruiter
- University Recruiter for an internship
- Campus Recruiter for an entry-level role
- Recruiter whose profile mentions the relevant
  job family

==================================================
RECRUITER AUTHENTICITY
==================================================

Determine whether this person genuinely appears
to be involved in recruiting or talent acquisition.

Examples:

Strong evidence:

- Recruiter
- Technical Recruiter
- Talent Acquisition
- University Recruiter
- Campus Recruiter
- Recruiting Manager
- Talent Partner

Weak/no evidence:

- Data Scientist
- Software Engineer
- Data Analyst
- Product Manager
- Developer
- Researcher

Set:

is_recruiter = true

when the evidence supports recruiting involvement.

Otherwise:

is_recruiter = false.

==================================================
SCORING
==================================================

Recruiter relevance score:

100 =
Clearly a recruiter AND strong evidence that
their recruiting scope is relevant to the job.

75 =
Clearly a recruiter with some relevant recruiting
signals, or a strong general recruiter.

50 =
Clearly a recruiter but little evidence about
their recruiting specialization.

25 =
Weak evidence of recruiting relevance.

0 =
Not actually a recruiter.

IMPORTANT:

Unknown specialization should NOT automatically
result in a low score.

==================================================
OVERALL SCORE
==================================================

LOCATION IS THE PRIMARY FACTOR.

Use:

overall_score =
    location_score * 0.70
    + recruiter_score * 0.30

If is_recruiter is false:

overall_score = 0

The final score must be between 0 and 100.

==================================================
REASONING
==================================================

Briefly explain:

1. How the recruiter location compares with the
   job location.

2. Why the person appears to be a recruiter.

3. Whether there is any additional evidence that
   their recruiting work is relevant to the job.

Remember:

Location is the primary factor.

Job-specific recruiting relevance is only an
additional advantage.

Do not invent information.
"""

            ranking = structured_llm.invoke(
                prompt
            )

            ranked.append(
                (
                    recruiter,
                    ranking.overall_score,
                )
            )

        # ==================================================
        # SORT
        # ==================================================

        ranked.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        # Return original Recruiter objects,
        # only reordered by ranking.

        return [
            recruiter
            for recruiter, score in ranked
        ]