from app.agents.recruiter_discovery import RecruiterDiscovery
from app.models.job import Job


def test_recruiter_discovery():

    job = Job(
        title="Data Scientist",
        company="Microsoft",
        location="Redmond, WA",
        description="Data Scientist position",
        required_skills=[
            "Python",
            "SQL",
            "Machine Learning",
        ],
    )

    discovery = RecruiterDiscovery()

    recruiters = discovery.discover(job)

    print("\n")
    print("=" * 60)
    print("RECRUITER DISCOVERY")
    print("=" * 60)

    for recruiter in recruiters:
        print(f"\nName: {recruiter.name}")
        print(f"Company: {recruiter.company}")
        print(f"LinkedIn: {recruiter.linkedin_url}")
        print(f"Source: {recruiter.source_url}")

    print("\n" + "=" * 60)

    assert isinstance(recruiters, list)