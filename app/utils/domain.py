from urllib.parse import urlparse


def extract_domain(url: str) -> str:

    parsed = urlparse(url)

    hostname = parsed.hostname

    if not hostname:
        raise ValueError(
            f"Could not extract domain from URL: {url}"
        )

    return hostname.replace("www.", "")