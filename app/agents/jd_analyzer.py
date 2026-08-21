from app.models.job import Job
from app.services.llm import get_llm


class JDAnalyzer:

    def __init__(self):
        self.llm = get_llm()

    def analyze(self, job_description: str) -> Job:

        structured_llm = self.llm.with_structured_output(Job)

        prompt = f"""
You are the Job Description Analyzer for an AI-powered
recruiter outreach system.

Analyze the job description below and extract structured information.

Extract:

1. Job title
2. Company
3. Location
4. Required skills
5. Preferred skills
6. Responsibilities
7. Qualifications
8. Important keywords

Rules:

- Only extract information supported by the job description.
- Do not invent company, location, skills, or qualifications.
- Keep skills concise.
- Separate required skills from preferred skills.
- Extract the most important keywords that will later help us
  match the job against a candidate's resume and projects.
- Preserve the complete original job description in the
  `description` field.

JOB DESCRIPTION:

{job_description}
"""

        result = structured_llm.invoke(prompt)

        return result