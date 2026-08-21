import os

import requests
from dotenv import load_dotenv

load_dotenv()


class DomainFinder:

    BASE_URL = "https://api.hunter.io/v2"

    def __init__(self):
        self.api_key = os.getenv("HUNTER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "HUNTER_API_KEY is not set in the .env file."
            )

    def find_domain(self, company: str) -> str:

        url = f"{self.BASE_URL}/domain-finder"

        params = {
            "company": company,
            "api_key": self.api_key,
            "perfect_match": True,
            "limit": 1,
        }

        response = requests.get(
            url,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json().get("data", [])

        if not data:
            raise ValueError(
                f"No domain found for company: {company}"
            )

        return data[0]["domain"]