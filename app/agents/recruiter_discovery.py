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

        # --------------------------------------------------
        # City-first searches
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Company-wide fallback
        #
        # Company remains fixed.
        # Location is broadened.
        # --------------------------------------------------

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

        def run_queries(queries, results):

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
        # STEP 2 — DEDUPLICATE CITY RESULTS
        # ==================================================

        city_unique_results = {}

        for result in results:

            url = result.get("href", "")

            if not url:
                continue

            if "linkedin.com/in/" not in url.lower():
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
        # STEP 3 — COMPANY-WIDE FALLBACK
        # ==================================================

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
        # STEP 4 — DEDUPLICATE ALL RESULTS
        # ==================================================

        unique_results = {}

        for result in results:

            url = result.get("href", "")

            if not url:
                continue

            if "linkedin.com/in/" not in url.lower():
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
        # STEP 5 — BASIC RECRUITER FILTERING
        # ==================================================

        recruiter_keywords = [
            "recruiter",
            "recruiting",
            "talent acquisition",
            "talent partner",
            "technical recruiter",
            "campus recruiter",
            "university recruiter",
            "university talent",
            "campus talent",
            "hiring",
            "talent management",
        ]

        non_recruiter_keywords = [
            "data scientist",
            "software engineer",
            "data analyst",
            "product manager",
            "machine learning engineer",
            "developer",
            "software developer",
            "research scientist",
            "business analyst",
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
        # STEP 6 — LLM EXTRACTION
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
from public search-engine results.

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

==================================================
COMPANY FILTER — CRITICAL
==================================================

The target company is:

{job.company}

Only return people who appear to work for
the target company.

The target company is a HARD FILTER.

Do NOT return a person simply because the
target company appears somewhere in the search
snippet.

Do NOT assume the person works for the target
company because the search query contained the
company name.

If the person's company is clearly another company,
do not return them.

If you cannot establish that the person works for
the target company, set company=null.

==================================================
RECRUITER FILTER
==================================================

Only return people who appear to be involved in:

- Recruiting
- Talent Acquisition
- Technical Recruiting
- Campus Recruiting
- University Recruiting
- Talent Partnerships
- Recruiting Management
- Hiring

Do NOT return:

- Data Scientists
- Data Analysts
- Software Engineers
- Machine Learning Engineers
- Product Managers
- Developers
- Researchers
- Other non-recruiting employees

==================================================
EXTRACTION RULES
==================================================

- Extract the person's actual full name.
- Do not include "LinkedIn" in the name.
- Do not include their professional headline in the name.
- Do not invent information.
- If a field is unavailable, return null.
- Preserve the LinkedIn URL exactly as provided.
- Use only information supported by the search result.
"""

        extracted = structured_llm.invoke(
            prompt
        )

        # ==================================================
        # STEP 7 — HARD COMPANY VALIDATION
        # ==================================================

        recruiters = []

        target_company = (
            job.company
            .lower()
            .strip()
        )

        seen_linkedin_urls = set()

        for person in extracted.recruiters:

            if not person.name:
                continue

            if not person.linkedin_url:
                continue

            # --------------------------------------------------
            # Company must be known.
            # --------------------------------------------------

            if not person.company:
                print(
                    f"Skipping {person.name}: "
                    f"company could not be established."
                )
                continue

            person_company = (
                person.company
                .lower()
                .strip()
            )

            # --------------------------------------------------
            # HARD COMPANY FILTER
            # --------------------------------------------------

            if person_company != target_company:

                print(
                    f"Skipping {person.name}: "
                    f"company mismatch "
                    f"({person.company} != {job.company})"
                )

                continue

            # --------------------------------------------------
            # Deduplicate
            # --------------------------------------------------

            linkedin_url = (
                person.linkedin_url.strip()
            )

            if linkedin_url in seen_linkedin_urls:
                continue

            seen_linkedin_urls.add(
                linkedin_url
            )

            # --------------------------------------------------
            # Create recruiter
            # --------------------------------------------------

            recruiters.append(
                Recruiter(
                    name=person.name,
                    title=person.title,
                    company=person.company,
                    location=person.location,
                    linkedin_url=linkedin_url,
                    source_url=linkedin_url,
                    confidence_score=0.0,
                )
            )

        # ==================================================
        # STEP 8 — CAP AT 10
        # ==================================================

        recruiters = recruiters[:10]

        print(
            f"Final validated recruiter pool: "
            f"{len(recruiters)}"
        )

        if not recruiters:

            raise ValueError(
                f"No valid recruiters associated with "
                f"{job.company} could be extracted."
            )

        return recruiters