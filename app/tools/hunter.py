import os

import requests
from dotenv import load_dotenv

from app.models.recruiter import RecruiterEmail

load_dotenv()


class HunterTool:

    BASE_URL = "https://api.hunter.io/v2"

    def __init__(self, api_key: str | None = None):
        self.api_key = (
            api_key or os.getenv("HUNTER_API_KEY") or ""
        ).strip()

        if not self.api_key:
            raise ValueError("A Hunter API key is required.")

    def find_email(
        self,
        first_name: str,
        last_name: str,
        company: str,
    ) -> RecruiterEmail:

        url = f"{self.BASE_URL}/email-finder"

        params = {
            "first_name": first_name,
            "last_name": last_name,
            "company": company,
            "api_key": self.api_key,
        }

        response = requests.get(
            url,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json().get("data", {})

        return RecruiterEmail(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            hunter_score=data.get("score"),
            verification_status=(
                data.get("verification", {})
                .get("status")
            ),
            company=data.get("company"),
            domain=data.get("domain"),
        )