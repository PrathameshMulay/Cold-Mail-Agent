from app.agents.jd_analyzer import JDAnalyzer


def test_jd_analyzer():

    job_description = """
    Data Scientist Intern

    Company: Example AI

    Location: Chicago, IL

    We are looking for a Data Scientist Intern to join our
    analytics team.

    Responsibilities:
    - Build machine learning models
    - Analyze large datasets
    - Develop data pipelines
    - Communicate insights to business stakeholders

    Required Qualifications:
    - Python
    - SQL
    - Pandas
    - Scikit-learn
    - Machine learning fundamentals

    Preferred Qualifications:
    - Experience with AWS
    - Experience with PySpark
    - Experience with NLP
    """

    analyzer = JDAnalyzer()

    job = analyzer.analyze(job_description)

    print("\n" + "=" * 50)
    print("JD ANALYSIS")
    print("=" * 50)

    print(f"\nTitle: {job.title}")
    print(f"Company: {job.company}")
    print(f"Location: {job.location}")

    print("\nRequired Skills:")
    for skill in job.required_skills:
        print(f"  - {skill}")

    print("\nPreferred Skills:")
    for skill in job.preferred_skills:
        print(f"  - {skill}")

    print("\nResponsibilities:")
    for responsibility in job.responsibilities:
        print(f"  - {responsibility}")

    print("\nQualifications:")
    for qualification in job.qualifications:
        print(f"  - {qualification}")

    print("\nKeywords:")
    for keyword in job.keywords:
        print(f"  - {keyword}")

    print("\n" + "=" * 50)

    assert job.title
    assert job.company
    assert job.required_skills
    assert job.responsibilities