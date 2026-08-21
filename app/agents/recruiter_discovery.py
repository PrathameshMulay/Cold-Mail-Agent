from typing import List

from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.recruiter import RecruiterExtractionList
from app.services.llm import get_llm
from app.tools.web_search import WebSearchTool


class RecruiterDiscovery:

    def __init__(self):
        self.search_tool = WebSearchTool()
        self.llm = get_llm()

    def discover(self, job: Job) -> List[Recruiter]:

        # ==================================================
        # SEARCH QUERIES
        # ==================================================

        city = job.location

        # City-first searches
        city_queries = []

        if city:
            city_queries = [
                f'site:linkedin.com/in/ '
                f'"{job.company}" recruiter "{city}"',

                f'site:linkedin.com/in/ '
                f'"{job.company}" "talent acquisition" "{city}"',

                f'site:linkedin.com/in/ '
                f'"{job.company}" recruiting "{city}"',

                f'site:linkedin.com/in/ '
                f'"{job.company}" "talent partner" "{city}"',
            ]

        # Company-wide fallback searches
        company_queries = [
            f'site:linkedin.com/in/ '
            f'"{job.company}" recruiter',

            f'site:linkedin.com/in/ '
            f'"{job.company}" "talent acquisition"',

            f'site:linkedin.com/in/ '
            f'"{job.company}" recruiting',

            f'site:linkedin.com/in/ '
            f'"{job.company}" "talent partner"',
        ]

        # ==================================================
        # SEARCH HELPER
        # ==================================================

        def run_queries(
            queries,
            results,
        ):

            for query in queries:

                try:

                    search_results = self.search_tool.search(
                        query=query,
                        max_results=15,
                    )

                    if search_results:
                        results.extend(search_results)

                except Exception as e:

                    print(
                        f"Search failed for query: {query}"
                    )

                    print(
                        f"Reason: {e}"
                    )

                    continue

            return results

        # ==================================================
        # STEP 1 — CITY SEARCH
        # ==================================================

        results = []

        if city:

            print(
                f"\nSearching for recruiters in {city}..."
            )

            results = run_queries(
                city_queries,
                results,
            )

        # ==================================================
        # DEDUPLICATE CITY RESULTS
        # ==================================================

        city_unique_results = {}

        for result in results:

            url = result.get("href", "")

            if not url:
                continue

            if "linkedin.com/in/" not in url:
                continue

            city_unique_results[url] = result

        city_results = list(
            city_unique_results.values()
        )

        print(
            f"City search returned "
            f"{len(city_results)} unique LinkedIn results."
        )

        # ==================================================
        # STEP 2 — COMPANY FALLBACK
        # ==================================================

        # We intentionally do NOT cap at 15 yet.
        #
        # We want to build a pool of actual recruiter
        # candidates first.

        if len(city_results) < 15:

            print(
                "Not enough city results. "
                "Running company-wide fallback searches..."
            )

            results = run_queries(
                company_queries,
                results,
            )

        # ==================================================
        # DEDUPLICATE ALL RESULTS
        # ==================================================

        unique_results = {}

        for result in results:

            url = result.get("href", "")

            if not url:
                continue

            if "linkedin.com/in/" not in url:
                continue

            unique_results[url] = result

        results = list(
            unique_results.values()
        )

        print(
            f"Total unique LinkedIn results: "
            f"{len(results)}"
        )

        if not results:

            raise ValueError(
                f"No recruiter search results found "
                f"for {job.company}."
            )

        # ==================================================
        # STEP 3 — BASIC RECRUITER FILTERING
        # ==================================================

        recruiter_keywords = [
            "recruiter",
            "recruiting",
            "talent acquisition",
            "talent partner",
            "technical recruiter",
            "campus recruiter",
            "university recruiter",
        ]

        non_recruiter_keywords = [
            "data scientist",
            "software engineer",
            "data analyst",
            "product manager",
            "machine learning engineer",
            "developer",
        ]

        recruiter_results = []

        for result in results:

            title = result.get(
                "title",
                "",
            )

            body = result.get(
                "body",
                "",
            )

            url = result.get(
                "href",
                "",
            )

            text = (
                f"{title} {body}"
            ).lower()

            # Must contain a recruiting signal.
            if not any(
                keyword in text
                for keyword in recruiter_keywords
            ):
                continue

            # Remove obvious non-recruiters.
            if any(
                keyword in text
                for keyword in non_recruiter_keywords
            ):
                continue

            recruiter_results.append(
                {
                    "title": title,
                    "body": body,
                    "url": url,
                }
            )

        print(
            f"Filtered recruiter candidates: "
            f"{len(recruiter_results)}"
        )

        if not recruiter_results:

            raise ValueError(
                f"Search returned results for "
                f"{job.company}, but none appeared "
                f"to be recruiters."
            )

        # ==================================================
        # STEP 4 — LLM EXTRACTION
        # ==================================================

        structured_llm = self.llm.with_structured_output(
            RecruiterExtractionList
        )

        results_text = ""

        for i, result in enumerate(
            recruiter_results,
            start=1,
        ):

            results_text += f"""
RESULT {i}

TITLE:
{result["title"]}

SNIPPET:
{result["body"]}

URL:
{result["url"]}

------------------------------
"""

        prompt = f"""
You are extracting structured information about recruiters
from search results for a job.

JOB
---
Company: {job.company}
Job Title: {job.title}
Location: {job.location}

SEARCH RESULTS
--------------

{results_text}

For each search result, determine:

1. Full name
2. Professional title
3. Company
4. Location, if available
5. LinkedIn URL

IMPORTANT:

- Extract the person's actual name.
- Do not include "LinkedIn" in the person's name.
- Do not include their professional headline in their name.
- Do not invent information.
- If a field is unavailable, return null.
- Preserve the LinkedIn URL exactly as provided.
- Only return people who appear to be recruiters,
  talent acquisition professionals, recruiting professionals,
  or hiring professionals.
- Do not return data scientists, engineers, analysts,
  product managers, or other non-recruiting professionals.
"""

        extracted = structured_llm.invoke(
            prompt
        )

        # ==================================================
        # STEP 5 — CREATE RECRUITER OBJECTS
        # ==================================================

        recruiters = []

        for person in extracted.recruiters:

            if not person.name:
                continue

            if not person.linkedin_url:
                continue

            recruiters.append(
                Recruiter(
                    name=person.name,
                    title=person.title,
                    company=person.company or job.company,
                    location=person.location,
                    linkedin_url=person.linkedin_url,
                    source_url=person.linkedin_url,
                    confidence_score=0.0,
                )
            )

        # ==================================================
        # STEP 6 — CAP AT 15 ACTUAL RECRUITERS
        # ==================================================

        recruiters = recruiters[:15]

        print(
            f"Final recruiter pool: "
            f"{len(recruiters)}"
        )

        if not recruiters:

            raise ValueError(
                f"No valid recruiters could be extracted "
                f"for {job.company}."
            )

        return recruiters