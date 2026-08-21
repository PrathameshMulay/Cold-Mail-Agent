from app.agents.recruiter_ranker import RecruiterRanker
from app.models.job import Job
from app.models.recruiter import Recruiter


def test_recruiter_ranker():

    job = Job(
        title="Data Scientist",
        company="Microsoft",
        location="Chicago, IL",
        description="Data Scientist position",
    )

    recruiters = [
        Recruiter(
            name="Jane Smith",
            title="Technical Recruiter",
            company="Microsoft",
            location="Chicago, IL",
            linkedin_url="https://linkedin.com/in/jane",
        ),
        Recruiter(
            name="John Doe",
            title="Technical Recruiter",
            company="Microsoft",
            location="Seattle, WA",
            linkedin_url="https://linkedin.com/in/john",
        ),
        Recruiter(
            name="Sarah Brown",
            title="Data Analyst",
            company="Microsoft",
            location="Chicago, IL",
            linkedin_url="https://linkedin.com/in/sarah",
        ),
    ]

    ranker = RecruiterRanker()

    ranked = ranker.rank(
        job,
        recruiters,
    )

    print("\n")
    print("=" * 60)
    print("RECRUITER LOCATION RANKING")
    print("=" * 60)

    for i, recruiter in enumerate(ranked, start=1):

        print(f"\n{i}. {recruiter.recruiter_name}")
        print(f"   Title: {recruiter.recruiter_title}")
        print(f"   Location: {recruiter.recruiter_location}")
        print(f"   Location Score: {recruiter.location_score}")
        print(f"   Overall Score: {recruiter.overall_score}")
        print(f"   Reason: {recruiter.reasoning}")

    print("\n" + "=" * 60)

    assert len(ranked) == 3

    assert (
        ranked[0].overall_score
        >= ranked[-1].overall_score
    )