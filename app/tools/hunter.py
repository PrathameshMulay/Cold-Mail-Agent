import os

import requests
from dotenv import load_dotenv

from app.models.recruiter import RecruiterEmail

load_dotenv()


class HunterTool:

    BASE_URL = "https://api.hunter.io/v2"

    def __init__(self):
        self.api_key = os.getenv("HUNTER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "HUNTER_API_KEY is not set in the .env file."
            )

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