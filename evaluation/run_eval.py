import json
from pathlib import Path
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
import argparse

sys.path.insert(0, str(PROJECT_ROOT))
from app.agents.jd_analyzer import JDAnalyzer
from app.agents.resume_analyzer import ResumeAnalyzer
from app.agents.recruiter_discovery import RecruiterDiscovery
from app.agents.recruiter_ranker import RecruiterRanker
from app.agents.evidence_matcher import EvidenceMatcher
from app.agents.email_generator import EmailGenerator


BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "datasets" / "eval_cases.json"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_PATH = RESULTS_DIR / "evaluation_results.json"


def load_cases():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def serialize(obj):
    """
    Convert Pydantic models / Python objects
    into JSON-serializable dictionaries.
    """

    if obj is None:
        return None

    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    if isinstance(obj, list):
        return [serialize(item) for item in obj]

    if isinstance(obj, dict):
        return {
            key: serialize(value)
            for key, value in obj.items()
        }

    return obj


def run_case(case):

    case_id = case["case_id"]

    job_description = case["job"]["description"]
    resume_text = case["resume"]["text"]

    print("\n" + "=" * 70)
    print(f"RUNNING {case_id}")
    print("=" * 70)

    result = {
        "case_id": case_id,
        "status": "success",
        "expected": case.get("expected", {}),
        "outputs": {},
    }

    # ==================================================
    # 1. JD ANALYZER
    # ==================================================

    print("\n[1/6] JD Analyzer")

    try:

        jd_analyzer = JDAnalyzer()

        job = jd_analyzer.analyze(
            job_description
        )

        result["outputs"]["job"] = serialize(job)

        print("✓ JD analysis complete")

    except Exception as e:

        result["outputs"]["job"] = {
            "error": str(e)
        }

        print(
            f"✗ JD Analyzer failed: {e}"
        )

    # ==================================================
    # 2. RESUME ANALYZER
    # ==================================================

    print("\n[2/6] Resume Analyzer")

    try:

        resume_analyzer = ResumeAnalyzer()

        candidate = resume_analyzer.analyze(
            resume_text
        )

        result["outputs"]["resume"] = serialize(
            candidate
        )

        print("✓ Resume analysis complete")

    except Exception as e:

        result["outputs"]["resume"] = {
            "error": str(e)
        }

        print(
            f"✗ Resume Analyzer failed: {e}"
        )

    # ==================================================
    # 3. RECRUITER DISCOVERY
    # ==================================================

    print("\n[3/6] Recruiter Discovery")

    try:

        if "job" not in result["outputs"]:

            raise ValueError(
                "JD analysis failed; "
                "cannot run recruiter discovery."
            )

        recruiters = RecruiterDiscovery().discover(
            job
        )

        result["outputs"]["recruiters"] = serialize(
            recruiters
        )

        print(
            f"✓ Found {len(recruiters)} recruiters"
        )

    except Exception as e:

        recruiters = []

        result["outputs"]["recruiters"] = {
            "error": str(e)
        }

        print(
            f"✗ Recruiter Discovery failed: {e}"
        )

    # ==================================================
    # 4. RECRUITER RANKER
    # ==================================================

    print("\n[4/6] Recruiter Ranker")

    try:

        if not recruiters:

            raise ValueError(
                "No recruiters available for ranking."
            )

        ranked_recruiters = RecruiterRanker().rank(
            job=job,
            recruiters=recruiters,
        )

        result["outputs"]["ranked_recruiters"] = serialize(
            ranked_recruiters
        )

        print(
            f"✓ Ranked {len(ranked_recruiters)} recruiters"
        )

    except Exception as e:

        ranked_recruiters = []

        result["outputs"]["ranked_recruiters"] = {
            "error": str(e)
        }

        print(
            f"✗ Recruiter Ranker failed: {e}"
        )

    # ==================================================
    # 5. EVIDENCE MATCHER
    # ==================================================

    print("\n[5/6] Evidence Matcher")

    try:

        evidence_matcher = EvidenceMatcher()

        evidence = evidence_matcher.match(
            job=job,
            candidate=candidate,
        )

        result["outputs"]["evidence"] = serialize(
            evidence
        )

        print("✓ Evidence matching complete")

    except Exception as e:

        result["outputs"]["evidence"] = {
            "error": str(e)
        }

        print(
            f"✗ Evidence Matcher failed: {e}"
        )

    # ==================================================
    # 6. EMAIL GENERATOR
    # ==================================================

    print("\n[6/6] Email Generator")

    try:

        if not ranked_recruiters:

            raise ValueError(
                "No ranked recruiter available "
                "for email generation."
            )

        # Use the highest-ranked recruiter
        # for evaluation purposes.
        selected_recruiter = ranked_recruiters[0]

        email_generator = EmailGenerator()

        email = email_generator.generate(
            job=job,
            candidate=candidate,
            recruiter=selected_recruiter,
            evidence=evidence,
        )

        result["outputs"]["email"] = serialize(
            email
        )

        print(
            "✓ Email generation complete"
        )

    except Exception as e:

        result["outputs"]["email"] = {
            "error": str(e)
        }

        print(
            f"✗ Email Generator failed: {e}"
        )

    return result


def run_evaluation(case_id=None):

    print("=" * 70)
    print("COLD MAIL AGENT — AI EVALUATION")
    print("=" * 70)

    cases = load_cases()

    # Run only the requested case
    if case_id:

        cases = [
            case
            for case in cases
            if case["case_id"] == case_id
        ]

        if not cases:
            raise ValueError(
                f"Case '{case_id}' not found in eval_cases.json"
            )

    print(
        f"\nRunning {len(cases)} evaluation case(s)."
    )

    results = []

    for case in cases:

        try:

            result = run_case(case)

            results.append(result)

        except Exception as e:

            results.append(
                {
                    "case_id": case["case_id"],
                    "status": "failed",
                    "error": str(e),
                }
            )

            print(
                f"\n✗ Case {case['case_id']} "
                f"failed unexpectedly: {e}"
            )

    # ==================================================
    # SAVE RESULTS
    # ==================================================

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Load existing results
    existing_results = []

    if RESULTS_PATH.exists():

        with open(
            RESULTS_PATH,
            "r",
            encoding="utf-8",
        ) as f:

            existing_results = json.load(f)

    # Remove previous result for the same case
    # so rerunning a case updates it instead
    completed_case_ids = {
        result["case_id"]
        for result in results
    }

    existing_results = [
        result
        for result in existing_results
        if result.get("case_id")
        not in completed_case_ids
    ]

    # Add new results
    existing_results.extend(results)

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            existing_results,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 70)
    print("EVALUATION RUN COMPLETE")
    print("=" * 70)

    print(
        f"Cases executed this run: {len(results)}"
    )

    print(
        f"Total saved results: {len(existing_results)}"
    )

    print(
        f"\nResults saved to:\n{RESULTS_PATH}"
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Run Cold Mail Agent evaluations"
    )

    parser.add_argument(
        "--case",
        type=str,
        help="Run a specific evaluation case, e.g. case_001",
    )

    args = parser.parse_args()

    run_evaluation(
        case_id=args.case
    )