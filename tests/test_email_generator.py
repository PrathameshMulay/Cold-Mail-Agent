from app.agents.email_generator import EmailGenerator
from app.agents.evidence_matcher import EvidenceMatcher
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter


def test_email_generator():

    # ==================================================
    # JOB
    # ==================================================

    job = Job(
        title="Data Scientist Intern",
        company="Microsoft",
        location="Chicago, IL",
        description="""
        We are looking for a Data Scientist Intern who can
        build machine learning models, analyze large datasets,
        develop data-driven solutions, and work with Python
        and SQL.

        The candidate should have experience with machine
        learning, statistical analysis, and data engineering.
        """,
        required_skills=[
            "Python",
            "SQL",
            "Machine Learning",
            "Data Analysis",
        ],
        preferred_skills=[
            "PySpark",
            "Airflow",
            "Deep Learning",
        ],
    )


    # ==================================================
    # RECRUITER
    # ==================================================

    recruiter = Recruiter(
        name="Jane Smith",
        title="Technical Recruiter",
        company="Microsoft",
        location="Chicago, IL",
        linkedin_url="https://linkedin.com/in/example",
    )


    # ==================================================
    # CANDIDATE
    # ==================================================

    candidate = Candidate(
        name="Prathamesh Sanjay Mulay",
        email="pmulay2@illinois.edu",

        education=[
            "University of Illinois Urbana-Champaign | "
            "MS in Information Management - Data Science & Analytics"
        ],

        skills=[
            "Python",
            "SQL",
            "PySpark",
            "Machine Learning",
            "Deep Learning",
            "Forecasting",
            "NLP",
            "Power BI",
            "Tableau",
        ],

        experience=[
            (
                "Built a patient-level demand forecasting model "
                "using Persistency, Compliance, and Dosing metrics, "
                "achieving less than 2% variance from actuals."
            ),

            (
                "Automated KPI dashboards using Tellius, "
                "reducing manual reporting effort by 8+ hours per week."
            ),

            (
                "Developed a prescriber classification model using "
                "HCP attributes, achieving 78% AUPRC."
            ),

            (
                "Forecasted patient compliance using ETS time-series "
                "modeling with 80% accuracy for a $300M annual sales brand."
            ),

            (
                "Designed physician segmentation and call-planning "
                "framework for an $800M annual revenue brand."
            ),
        ],

        projects=[
            (
                "Built a hybrid LSTM and GCN model for fraud detection."
            ),

            (
                "Built KPI-driven Tableau views for 9K events across "
                "10 states and analyzed 19.1M+ social engagements."
            ),

            (
                "Developed a data engineering pipeline using "
                "PySpark and Airflow."
            ),
        ],

        achievements=[
            "Achieved <2% variance from actuals in patient demand forecasting.",

            "Reduced manual reporting effort by 8+ hours per week.",

            "Achieved 78% AUPRC in prescriber classification.",

            "Achieved 80% forecasting accuracy for a $300M annual sales brand.",

            "Supported an $800M annual revenue brand.",

            "Achieved 83% defect detection accuracy.",
        ],
    )


    # ==================================================
    # STEP 1 — EVIDENCE MATCHING
    # ==================================================

    matcher = EvidenceMatcher()

    evidence = matcher.match(
        job=job,
        candidate=candidate,
    )


    # ==================================================
    # PRINT SELECTED EVIDENCE
    # ==================================================

    print("\n")
    print("=" * 70)
    print("EVIDENCE SELECTED FOR EMAIL")
    print("=" * 70)

    for i, match in enumerate(evidence.matches, start=1):

        print(f"\n{i}. {match.capability}")
        print(f"Evidence: {match.evidence}")
        print(f"Why relevant: {match.relevance_reason}")
        print(f"Score: {match.score}")

    print("\n" + "=" * 70)


    # ==================================================
    # STEP 2 — EMAIL GENERATION
    # ==================================================

    generator = EmailGenerator()

    email = generator.generate(
        job=job,
        recruiter=recruiter,
        candidate=candidate,
        evidence=evidence,
    )


    # ==================================================
    # PRINT EMAIL
    # ==================================================

    print("\n")
    print("=" * 70)
    print("GENERATED COLD EMAIL")
    print("=" * 70)

    print("\nSubject:")
    print(email.subject)

    print("\nBody:")
    print(repr(email.body))

    print("\n" + "=" * 70)


    # ==================================================
    # VALIDATION
    # ==================================================

    assert evidence.matches
    assert len(evidence.matches) <= 4

    assert email.subject
    assert email.body