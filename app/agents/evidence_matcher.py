from app.models.candidate import Candidate
from app.models.evidence import EvidenceSelection
from app.models.job import Job
from app.services.llm import get_llm


class EvidenceMatcher:

    def __init__(self):
        self.llm = get_llm()

    def match(
        self,
        job: Job,
        candidate: Candidate,
    ) -> EvidenceSelection:

        structured_llm = self.llm.with_structured_output(
            EvidenceSelection
        )

        prompt = f"""
You are a recruiting evidence-matching agent.

Your task is to identify the strongest evidence from a
candidate's background that demonstrates their ability
to perform a specific job.

JOB TITLE:
{job.title}

JOB DESCRIPTION:
{job.description}

REQUIRED SKILLS:
{", ".join(job.required_skills)}

PREFERRED SKILLS:
{", ".join(job.preferred_skills)}

CANDIDATE EXPERIENCE:
{chr(10).join(candidate.experience)}

CANDIDATE PROJECTS:
{chr(10).join(candidate.projects)}

CANDIDATE ACHIEVEMENTS:
{chr(10).join(candidate.achievements)}

CANDIDATE SKILLS:
{chr(10).join(candidate.skills)}

Find the 3-4 strongest pieces of evidence.

Prioritize:

1. Direct match to job responsibilities.
2. Quantified achievements.
3. Business impact.
4. Relevant scale.
5. Technical complexity.
6. Relevant projects.

IMPORTANT:

Use the candidate's exact evidence.

Do not summarize away metrics.

For example:

"Built a patient-level demand forecasting model
achieving <2% variance from actuals"

is stronger than:

"Experienced in forecasting."

"Automated KPI dashboards reducing manual reporting
effort by 8+ hours/week"

is stronger than:

"Built dashboards."

Never invent information.

Each match must explain WHY the evidence is relevant
to this specific job.

Return 3-4 strongest matches.
"""

        return structured_llm.invoke(prompt)