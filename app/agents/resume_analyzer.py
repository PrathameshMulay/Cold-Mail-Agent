from app.models.candidate import Candidate
from app.services.llm import get_llm


class ResumeAnalyzer:

    def __init__(self):
        self.llm = get_llm()

    def analyze(self, resume_text: str) -> Candidate:

        structured_llm = self.llm.with_structured_output(
            Candidate
        )

        prompt = f"""
You are an expert resume parser.

Extract a structured candidate profile from the resume below.

Your most important responsibility is to PRESERVE SPECIFIC
EVIDENCE from the resume.

Do not summarize away numbers, metrics, scale, technologies,
business impact, or concrete outcomes.

==================================================
INFORMATION TO EXTRACT
==================================================

1. Candidate name

2. Email address

3. Education

4. Skills

5. Professional experience

6. Projects

7. Achievements / measurable outcomes


==================================================
EXPERIENCE EXTRACTION
==================================================

For every important experience, preserve:

- Company
- Job title
- What the candidate built or did
- Technologies/methods used
- Business problem
- Quantitative results
- Scale
- Business impact

Keep the original evidence as much as possible.

For example, if the resume says:

"Built a patient-level demand forecasting model and achieved
less than 2% variance from actuals."

DO NOT reduce it to:

"Built forecasting models."

Instead preserve:

"Built a patient-level demand forecasting model; achieved
less than 2% variance from actuals."


==================================================
QUANTITATIVE EVIDENCE
==================================================

Preserve ALL meaningful numbers from the resume.

Examples include:

- Percentages
- Accuracy
- AUPRC
- Revenue
- Cost savings
- Time savings
- Dataset size
- Number of users
- Number of records
- Years of experience
- Performance improvements
- Model metrics
- Scale of projects

Never remove a metric just because it appears inside a
longer sentence.

Never invent a metric.


==================================================
ACHIEVEMENTS
==================================================

Extract important measurable outcomes separately into
the achievements field.

Examples:

"Achieved <2% variance from actuals."

"Reduced manual reporting effort by 8+ hours per week."

"Achieved 80% forecasting accuracy."

"Supported a brand with approximately $300M in annual sales."

If an achievement is already part of an experience bullet,
it may also remain inside experience.

Do not create achievements that are not explicitly supported
by the resume.


==================================================
SKILLS
==================================================

Extract technical and professional skills explicitly present
in the resume.

Examples:

Python
SQL
PySpark
Machine Learning
Deep Learning
Power BI
Tableau
Airflow

Do not infer skills solely because the candidate worked on
a project that might normally require them.


==================================================
PROJECTS
==================================================

For each important project, preserve:

- Project name
- Problem being solved
- Methods/models used
- Technologies
- Important results
- Dataset/project scale when available


==================================================
RULES
==================================================

1. Use ONLY information explicitly contained in the resume.

2. Do not invent information.

3. Do not exaggerate achievements.

4. Do not remove quantitative evidence.

5. Do not replace specific achievements with generic summaries.

6. Preserve technical terminology.

7. Preserve business context.

8. Preserve measurable outcomes.

9. Keep experience concise enough to be useful to another
   AI agent, but detailed enough to retain evidence.

10. The resulting profile will be used to write personalized
    job application emails, so evidence and measurable impact
    are more important than generic descriptions.

RESUME:

{resume_text}
"""

        result = structured_llm.invoke(prompt)

        return result