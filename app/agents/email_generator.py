from app.models.candidate import Candidate
from app.models.email import ColdEmail
from app.models.evidence import EvidenceSelection
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.services.llm import get_llm


class EmailGenerator:

    def __init__(self):
        self.llm = get_llm()

    def generate(
        self,
        job: Job,
        recruiter: Recruiter,
        candidate: Candidate,
        evidence: EvidenceSelection,
    ) -> ColdEmail:

        structured_llm = self.llm.with_structured_output(
            ColdEmail
        )

        # Convert selected evidence into text for the LLM
        selected_evidence = "\n\n".join(
            [
                f"- {match.capability}: {match.evidence}\n"
                f"Why relevant: {match.relevance_reason}"
                for match in evidence.matches
            ]
        )

        prompt = f"""
You are an expert at writing personalized professional
cold emails to recruiters.

Your task is to write an email from the candidate to the
recruiter about the specific job below.

The email should feel like a strong, personalized application
outreach email rather than a generic cover letter.

==================================================
RECRUITER
==================================================

Name: {recruiter.name}
Title: {recruiter.title}
Company: {recruiter.company}


==================================================
JOB
==================================================

Title: {job.title}
Company: {job.company}
Location: {job.location}

JOB DESCRIPTION:

{job.description}

REQUIRED SKILLS:

{", ".join(job.required_skills)}

PREFERRED SKILLS:

{", ".join(job.preferred_skills)}


==================================================
CANDIDATE
==================================================

Name: {candidate.name}

Education:
{chr(10).join(candidate.education)}

Skills:
{chr(10).join(candidate.skills)}

Experience:
{chr(10).join(candidate.experience)}

Projects:
{chr(10).join(candidate.projects)}

Achievements:
{chr(10).join(candidate.achievements)}


==================================================
SELECTED EVIDENCE FOR THIS JOB
==================================================

The following evidence has already been selected because
it is highly relevant to this specific job.

Use this evidence as the PRIMARY factual basis for the
email.

{selected_evidence}


==================================================
IMPORTANT EVIDENCE RULES
==================================================

1. Use the SELECTED EVIDENCE above when writing the
   evidence bullets.

2. Do not replace specific evidence with generic statements.

3. Preserve quantitative results exactly.

4. Do not invent metrics or achievements.

5. Do not exaggerate the candidate's experience.

6. Each evidence bullet should communicate:

   CAPABILITY
   +
   SPECIFIC EVIDENCE
   +
   RESULT / SCALE / IMPACT when available.

For example:

BAD:
"Machine Learning: Experienced in machine learning."

GOOD:
"Machine Learning: Built a patient-level demand forecasting
model achieving less than 2% variance from actuals."

BAD:
"Data Engineering: Experienced with PySpark."

GOOD:
"Data Engineering: Developed a data engineering pipeline
using PySpark and Airflow."

BAD:
"Analytics: Strong analytical skills."

GOOD:
"Analytics: Automated KPI dashboards, reducing manual
reporting effort by 8+ hours per week."


==================================================
EMAIL STRUCTURE
==================================================

Use the following structure:

1. GREETING

Hi [Recruiter's first name],

2. OPENING

Mention that the candidate recently applied for the exact
job title and company.

Keep this to 1-2 sentences.

3. FIT STATEMENT

Briefly explain why the candidate is relevant to the role.

4. EVIDENCE

Use:

Key highlights of my experience include:

Then provide 3-4 bullets based primarily on the
SELECTED EVIDENCE.

5. ROLE CONNECTION

Write one short paragraph explaining why the candidate's
background connects specifically to this opportunity.

Base this on the actual job description.

Do not invent details about the team.

Do not use generic company praise.

6. CALL TO ACTION

End with a concise request to connect and discuss the
application.

7. SIGNATURE

Best regards,

[Candidate Name]


==================================================
PERSONALIZATION
==================================================

The email must be personalized to THIS job.

Use the job description to determine the language and
emphasis of the email.

For technical/Data Science roles, emphasize relevant:
- Machine learning
- Data engineering
- Statistical modeling
- Analytical work
- Technical projects
- Quantitative results

For analytics/consulting roles, emphasize relevant:
- Business problem solving
- Forecasting
- Segmentation
- Business impact
- Scale
- Stakeholder/client experience

For product/AI roles, emphasize relevant:
- AI/ML
- Product thinking
- Business impact
- Strategy
- Technical understanding
- Stakeholder experience

Do not use the same generic positioning for every job.


==================================================
WRITING STYLE
==================================================

The email should:

- Sound like a real person.
- Be confident but professional.
- Be concise.
- Focus on evidence rather than adjectives.
- Demonstrate relevance rather than simply claiming it.
- Avoid unnecessary technical explanations.

Target approximately 180-250 words.

Do NOT:

- Repeat the resume chronologically.
- List every skill.
- Mention irrelevant experience.
- Repeat the same qualification multiple times.
- Use excessive buzzwords.
- Use generic company praise.
- Ask directly for a referral.
- Pressure the recruiter.

Do not use:

"I hope this email finds you well."

"dream company"

"perfect fit"

"extremely excited"

"amazing company"

"leading company"

Excessive exclamation marks.


==================================================
FORMATTING
==================================================

Return the email body as properly formatted plain text.

Use actual line breaks.

Example structure:

Hi Jane,

I recently applied for the Data Scientist Intern position
at Microsoft and wanted to reach out to express my interest
in the opportunity.

I believe I am a strong fit for the role because I bring
relevant experience in machine learning, analytics, and
data engineering.

Key highlights of my experience include:

- **Machine Learning:** Built ...
- **Data Engineering:** Developed ...
- **Analytics:** Achieved ...

[Role-specific closing paragraph.]

I would appreciate the opportunity to connect and discuss
my application.

Best regards,

Prathamesh Mulay

Formatting rules:

- Put a blank line between paragraphs.
- Put each bullet on its own line.
- Do not put the entire email on one line.
- Do not wrap the email in quotation marks.
- Do not return code fences.
- Do not include "Body:" or "Email:" labels.
- Do not mention that AI generated the email.

Return only the subject and body.
"""

        result = structured_llm.invoke(prompt)

        return result