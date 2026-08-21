from app.tools.domain_finder import DomainFinder


def test_domain_finder():

    finder = DomainFinder()

    domain = finder.find_domain("Microsoft")

    print("\n")
    print("=" * 50)
    print("DOMAIN FINDER RESULT")
    print("=" * 50)

    print(f"Company: Microsoft")
    print(f"Domain: {domain}")

    print("=" * 50)

    assert domain
    assert domain == "microsoft.com"