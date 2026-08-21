from typing import Dict, Any

from app.agents.jd_analyzer import JDAnalyzer
from app.agents.resume_analyzer import ResumeAnalyzer
from app.agents.recruiter_discovery import RecruiterDiscovery
from app.agents.recruiter_ranker import RecruiterRanker
from app.agents.evidence_matcher import EvidenceMatcher
from app.agents.email_generator import EmailGenerator
from app.tools.hunter import HunterTool


class ColdMailPipeline:

    def __init__(self):

        self.jd_analyzer = JDAnalyzer()
        self.resume_analyzer = ResumeAnalyzer()
        self.recruiter_discovery = RecruiterDiscovery()
        self.recruiter_ranker = RecruiterRanker()
        self.evidence_matcher = EvidenceMatcher()
        self.email_generator = EmailGenerator()
        self.hunter = HunterTool()

    # ==========================================================
    # STAGE 1
    # ANALYZE JD + RESUME + FIND/RANK RECRUITERS
    # ==========================================================

    def find_recruiters(
        self,
        job_description: str,
        resume_text: str,
    ) -> Dict[str, Any]:

        # ------------------------------------------------------
        # STEP 1 — ANALYZE JOB
        # ------------------------------------------------------

        job = self.jd_analyzer.analyze(
            job_description
        )

        print("\n[1/4] Job analyzed")

        # ------------------------------------------------------
        # STEP 2 — ANALYZE RESUME
        # ------------------------------------------------------

        candidate = self.resume_analyzer.analyze(
            resume_text
        )

        print("[2/4] Resume analyzed")

        # ------------------------------------------------------
        # STEP 3 — DISCOVER RECRUITERS
        # ------------------------------------------------------

        recruiters = self.recruiter_discovery.discover(
            job
        )

        if not recruiters:
            raise ValueError(
                "No recruiters found for this job."
            )

        print(
            f"[3/4] Found {len(recruiters)} recruiters"
        )

        # ------------------------------------------------------
        # STEP 4 — RANK RECRUITERS
        # ------------------------------------------------------

        ranked_recruiters = self.recruiter_ranker.rank(
            job,
            recruiters
        )

        if not ranked_recruiters:
            raise ValueError(
                "No recruiters available after ranking."
            )

        print(
            f"[4/4] Ranked {len(ranked_recruiters)} recruiters"
        )

        return {
            "job": job,
            "candidate": candidate,
            "recruiters": ranked_recruiters,
        }

    # ==========================================================
    # STAGE 2
    # SELECTED RECRUITER → HUNTER → EVIDENCE → EMAIL
    # ==========================================================

    def generate_email(
        self,
        job,
        candidate,
        recruiter,
    ) -> Dict[str, Any]:

        # ------------------------------------------------------
        # STEP 1 — FIND EMAIL WITH HUNTER
        # ------------------------------------------------------

        name_parts = recruiter.name.split()

        if len(name_parts) < 2:
            raise ValueError(
                f"Unable to split recruiter name: "
                f"{recruiter.name}"
            )

        first_name = name_parts[0]
        last_name = name_parts[-1]

        print("\n" + "=" * 60)
        print("HUNTER INPUT")
        print("=" * 60)
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Company: {recruiter.company}")
        print("=" * 60)

        contact = self.hunter.find_email(
            first_name=first_name,
            last_name=last_name,
            company=recruiter.company,
        )

        print(
            f"[1/3] Hunter email lookup complete: "
            f"{contact.email}"
        )

        # ------------------------------------------------------
        # STEP 2 — MATCH EVIDENCE
        # ------------------------------------------------------

        evidence = self.evidence_matcher.match(
            job=job,
            candidate=candidate,
        )

        print(
            f"[2/3] Selected "
            f"{len(evidence.matches)} evidence points"
        )

        # ------------------------------------------------------
        # STEP 3 — GENERATE EMAIL
        # ------------------------------------------------------

        email = self.email_generator.generate(
            job=job,
            recruiter=recruiter,
            candidate=candidate,
            evidence=evidence,
        )

        print("[3/3] Email generated")

        return {
            "recruiter": recruiter,
            "contact": contact,
            "evidence": evidence,
            "email": email,
        }

    # ==========================================================
    # BACKWARD-COMPATIBLE FULL PIPELINE
    # ==========================================================

    def run(
        self,
        job_description: str,
        resume_text: str,
    ) -> Dict[str, Any]:

        # Stage 1
        recruiter_result = self.find_recruiters(
            job_description=job_description,
            resume_text=resume_text,
        )

        job = recruiter_result["job"]
        candidate = recruiter_result["candidate"]
        recruiters = recruiter_result["recruiters"]

        # Default to top-ranked recruiter.
        recruiter = recruiters[0]

        # Stage 2
        email_result = self.generate_email(
            job=job,
            candidate=candidate,
            recruiter=recruiter,
        )

        return {
            "job": job,
            "candidate": candidate,
            "recruiters": recruiters,
            "recruiter": recruiter,
            "contact": email_result["contact"],
            "evidence": email_result["evidence"],
            "email": email_result["email"],
        }