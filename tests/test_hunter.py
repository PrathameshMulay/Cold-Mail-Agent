from app.tools.hunter import HunterTool


def test_hunter():

    hunter = HunterTool()

    result = hunter.find_email(
        first_name="Jane",
        last_name="Smith",
        company="Microsoft",
    )

    print("\n")
    print("=" * 60)
    print("HUNTER EMAIL FINDER")
    print("=" * 60)

    print(f"First Name: {result.first_name}")
    print(f"Last Name: {result.last_name}")
    print(f"Email: {result.email}")
    print(f"Hunter Score: {result.hunter_score}")
    print(f"Company: {result.company}")
    print(f"Domain: {result.domain}")
    print(f"Verification: {result.verification_status}")

    print("=" * 60)

    assert result.email