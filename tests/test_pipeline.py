from app.workflow.pipeline import ColdMailPipeline


def test_cold_mail_pipeline():

    job_description = """
    Data Scientist Intern

    Microsoft is looking for a Data Scientist Intern who can
    build machine learning models, analyze large datasets,
    develop data-driven solutions, and work with Python and SQL.

    Candidates should have experience with machine learning,
    statistical analysis, and data engineering.

    Preferred experience includes PySpark, Airflow, and
    deep learning.
    """

    resume_text = """
    Prathamesh Sanjay Mulay
    pmulay2@illinois.edu

    EDUCATION

    University of Illinois Urbana-Champaign
    MS in Information Management - Data Science & Analytics

    EXPERIENCE

    ZS Associates Pvt Ltd
    Decision Analytics Associate

    Built a patient-level demand forecasting model using
    Persistency, Compliance, and Dosing metrics, achieving
    less than 2% variance from actuals.

    Automated KPI dashboards using Tellius, reducing manual
    reporting effort by 8+ hours per week.

    Developed a prescriber classification model using HCP
    attributes, achieving 78% AUPRC.

    Forecasted patient compliance using ETS time-series
    modeling with 80% accuracy for a $300M annual sales brand.

    Designed physician segmentation and call-planning
    framework for an $800M annual revenue brand.

    PROJECTS

    Built a hybrid LSTM and GCN model for fraud detection.

    Developed a data engineering pipeline using PySpark
    and Airflow.

    SKILLS

    Python, SQL, PySpark, Machine Learning,
    Deep Learning, Airflow, Forecasting
    """

    pipeline = ColdMailPipeline()

    result = pipeline.run(
        job_description=job_description,
        resume_text=resume_text,
    )

    print("\n")
    print("=" * 70)
    print("FINAL PIPELINE RESULT")
    print("=" * 70)

    print("\nRecruiter:")
    print(result["recruiter"])

    print("\nContact:")
    print(result["contact"])

    print("\nEvidence:")
    for match in result["evidence"].matches:
        print(
            f"- {match.capability}: "
            f"{match.evidence}"
        )

    print("\nSubject:")
    print(result["email"].subject)

    print("\nBody:")
    print(result["email"].body)

    print("\n" + "=" * 70)

    assert result["job"]
    assert result["candidate"]
    assert result["recruiter"]
    assert result["contact"].email
    assert result["evidence"].matches
    assert result["email"].subject
    assert result["email"].body