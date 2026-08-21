from app.agents.resume_analyzer import ResumeAnalyzer


def test_resume_analyzer():

    resume = """
    Prathamesh Sanjay Mulay
pmulay2@illinois.edu | LinkedIN | +1 (217) 766-0786 | Champaign, IL (open to relocation)
Education
University of Illinois, Urbana Champaign | Champaign, USA Aug 2025- May 2027
MS in Information Management - Data Science & Analytics – GPA : 4.0/4.0
Courses: Data-Statistics and Information, Information Consulting, Data Warehousing and BI, Database Design and Prototyping
Pune University | Pune, India BE in Mechanical Engineering with Minors in Artificial Intelligence and Machine Learning - GPA: 3.64/4.0
Courses: Operations Research, IOT, Statistical Computing, Regression and Classification, Data Analytics
Aug 2019 - Jun 2023
Skills
● Business Tools: Excel (PivotTables, Reporting), PowerPoint
● Programming: Python, SQL, SAS, R
● Analytics & Modeling: Statistics, Regression, Classification, EDA, Forecasting, Feature Engineering, Pandas, Numpy,
Seaborn, Pyspark, Data Mining, Machine Learning, Data Modelling, A/B Testing, Cloud computing, NLP
● Visualization: Matplotlib, SHAP, Tellius, PowerBI, Tableau, SAP BI
Professional Experience
Business Intelligence Group | Technology Consultant | Champaign, IL Feb 2026 – Present
• Initiate the transition from fragmented Excel-based grant reporting toward a centralized SQL database, currently defining
relational schemas and data integration workflows to support scalable analytics.
• Architect and prototype a three-layer system (backend database, structured frontend interface, automated reporting
layer) to standardize data capture and lay the foundation for analytics-ready reporting.
ZS Associates Pvt LTD | Decision Analytics Associate | Pune, India Aug 2023 – Jun 2025
● Delivered advanced analytics solutions for leading pharmaceutical clients, supporting commercial strategy and decision-
making in the healthcare and life sciences sector.
● Computed a demand forecasting model using patient metrics such as Persistency, Compliance and Dosing with variance
of less than 2% with that of actuals.
● Automated KPI dashboards using Tellius, integrating patient metrics and brand performance; reduced manual reporting
effort by 8+ hours/week, providing real time insights for commercial teams.
● Developed a prescriber classification model using HCP characteristics; achieved AUPRC of 78% resulting in targeting
precision and sales rep efficiency; visualised crucial data features using SHAP plot.
● Forecasted patient compliance using ETS time series modeling with 80% accuracy, influencing adherence strategies for a
brand with nearly $300M in annual sales.
● Designed and implemented an analytical framework for physician segmentation and call planning in collaboration with
key stakeholders, resulting in enhanced targeting accuracy of high-potential physicians by sales representatives for an
$800 million annual revenue brand at a major pharmaceutical company.
Bosch Chassis Systems Ltd | Analyst Intern – Digitalization | Pune, India Aug 2022 - Oct 2022
• Built a regression model to assess master cylinder quality (83% defect detection accuracy) and identified key defect
drivers, contributing to improved production consistency.
Academic Projects
Ticketmaster Event Analytics
• Event Sponsorship & Financial Performance Dashboard:
Built KPI-driven Tableau views for 9K events across 10 states, analyzing expected revenue, average ticket price, and
revenue per event, uncovering that Arts and Music outperform in revenue despite lower volume, while Sports show
inconsistent monetization.
• Event Social Engagement Analysis Dashboard:
Analyzed 19.1M+ social engagements by genre, venue, and geography, identifying Sports and Basketball as engagement
leaders, metro venues as high-impact locations, and a small set of events driving disproportionate reach.
Content-Based Recommendation System
• Built a content-based recommendation system using NLP techniques, applying text preprocessing and Porter
stemming for feature normalization.
• Used Count Vectorizer to transform text into numerical vectors and implemented cosine similarity to generate
personalized recommendations in Python.
Certifications
Oracle Cloud Infrastructure 2025: Data Science Professional Learned Machine Learning Life Cycle, MLOps, and Data Science workflows on Oracle Cloud platform.
    """

    analyzer = ResumeAnalyzer()

    candidate = analyzer.analyze(resume)

    print("\n")
    print("=" * 60)
    print("CANDIDATE PROFILE")
    print("=" * 60)

    print(f"\nName: {candidate.name}")
    print(f"Email: {candidate.email}")

    print("\nEducation:")
    for item in candidate.education:
        print(f"  - {item}")

    print("\nSkills:")
    for item in candidate.skills:
        print(f"  - {item}")

    print("\nExperience:")
    for item in candidate.experience:
        print(f"  - {item}")

    print("\nProjects:")
    for item in candidate.projects:
        print(f"  - {item}")

    print("\nAchievements:")
    for item in candidate.achievements:
        print(f"  - {item}")

    print("\n" + "=" * 60)

    assert candidate.name
    assert candidate.email
    assert candidate.skills
    assert candidate.achievements