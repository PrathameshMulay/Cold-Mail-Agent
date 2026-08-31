import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "datasets" / "eval_cases.json"
RESULTS_PATH = BASE_DIR / "results" / "evaluation_results.json"
REPORT_PATH = BASE_DIR / "results" / "evaluation_report.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(value):
    if value is None:
        return ""

    return str(value).strip().lower()


def contains_text(text, expected):
    return normalize(expected) in normalize(text)


def evaluate_job_analysis(expected, actual):
    scores = {}

    expected_job = expected.get("job", {})
    actual_job = actual or {}

    fields = [
        "company",
        "title",
        "location",
    ]

    for field in fields:

        expected_value = expected_job.get(field)
        actual_value = actual_job.get(field)

        if not expected_value:
            continue

        scores[field] = (
            1
            if contains_text(actual_value, expected_value)
            else 0
        )

    required_skills = expected_job.get(
        "required_skills",
        []
    )

    if required_skills:

        actual_skills = actual_job.get(
            "required_skills",
            []
        )

        matched = sum(
            1
            for skill in required_skills
            if any(
                normalize(skill) in normalize(actual_skill)
                or normalize(actual_skill) in normalize(skill)
                for actual_skill in actual_skills
            )
        )

        scores["required_skills"] = (
            matched / len(required_skills)
        )

    if not scores:
        return 0.0

    return sum(scores.values()) / len(scores)


def evaluate_resume_analysis(expected, actual):
    expected_resume = expected.get(
        "resume_analysis",
        {}
    )

    if not expected_resume:
        return None

    actual = actual or {}

    scores = []

    expected_name = expected_resume.get(
        "candidate_name"
    )

    if expected_name:
        scores.append(
            1
            if contains_text(
                actual.get("candidate_name"),
                expected_name,
            )
            else 0
        )

    expected_skills = expected_resume.get(
        "skills",
        []
    )

    if expected_skills:

        actual_skills = actual.get(
            "skills",
            []
        )

        matched = sum(
            1
            for skill in expected_skills
            if any(
                normalize(skill) in normalize(actual_skill)
                or normalize(actual_skill) in normalize(skill)
                for actual_skill in actual_skills
            )
        )

        scores.append(
            matched / len(expected_skills)
        )

    if not scores:
        return None

    return sum(scores) / len(scores)


def evaluate_recruiters(expected, actual):
    expected_recruiter = expected.get(
        "recruiter",
        {}
    )

    if not expected_recruiter:
        return None

    if not isinstance(actual, list):
        return 0.0

    if not actual:
        return 0.0

    expected_company = normalize(
        expected_recruiter.get("company")
    )

    valid_recruiters = 0

    for recruiter in actual:

        company = normalize(
            recruiter.get("company")
        )

        if expected_company:
            if expected_company not in company:
                continue

        valid_recruiters += 1

    # Precision@10
    return min(
        valid_recruiters / min(len(actual), 10),
        1.0,
    )


def evaluate_evidence(expected, actual):
    expected_evidence = expected.get(
        "evidence",
        []
    )

    if not expected_evidence:
        return None

    if not actual:
        return 0.0

    # EvidenceSelection may be a dictionary containing
    # a list of evidence matches.
    if isinstance(actual, dict):

        possible_lists = [
            "matches",
            "evidence",
            "selected_evidence",
            "evidence_matches",
        ]

        actual_items = []

        for key in possible_lists:

            value = actual.get(key)

            if isinstance(value, list):
                actual_items = value
                break

    elif isinstance(actual, list):

        actual_items = actual

    else:
        actual_items = []

    if not actual_items:
        return 0.0

    actual_text = " ".join(
        str(item)
        for item in actual_items
    ).lower()

    matched = sum(
        1
        for evidence in expected_evidence
        if normalize(evidence) in actual_text
        or any(
            word in actual_text
            for word in normalize(evidence).split()
            if len(word) > 4
        )
    )

    return min(
        matched / len(expected_evidence),
        1.0,
    )


def evaluate_email(expected, actual):
    email_expectations = expected.get(
        "email",
        {}
    )

    if not email_expectations:
        return None

    if not actual:
        return 0.0

    if isinstance(actual, dict):

        email_text = " ".join(
            str(value)
            for value in actual.values()
        )

    else:

        email_text = str(actual)

    email_text = normalize(email_text)

    checks = []

    if email_expectations.get(
        "must_mention_job"
    ):

        title = expected.get(
            "job",
            {}
        ).get("title")

        if title:
            checks.append(
                1
                if normalize(title) in email_text
                else 0
            )

    if email_expectations.get(
        "must_mention_company"
    ):

        company = expected.get(
            "job",
            {}
        ).get("company")

        if company:
            checks.append(
                1
                if normalize(company) in email_text
                else 0
            )

    # We cannot prove factuality with simple string
    # matching. That will be handled by the LLM judge
    # in the next evaluation layer.
    #
    # For now, record that the email exists.

    if email_text:
        checks.append(1)

    if not checks:
        return 0.0

    return sum(checks) / len(checks)


def evaluate_case(case, result):

    expected = case.get(
        "expected",
        {}
    )

    outputs = result.get(
        "outputs",
        {}
    )

    evaluation = {}

    evaluation["job_analysis_score"] = (
        evaluate_job_analysis(
            expected,
            outputs.get("job"),
        )
    )

    evaluation["resume_analysis_score"] = (
        evaluate_resume_analysis(
            expected,
            outputs.get("candidate")
            or outputs.get("resume"),
        )
    )

    evaluation["recruiter_discovery_score"] = (
        evaluate_recruiters(
            expected,
            outputs.get("recruiters"),
        )
    )

    # Ranking is evaluated separately once we
    # add ranking-specific ground truth.
    evaluation["recruiter_ranking_score"] = None

    evaluation["evidence_score"] = (
        evaluate_evidence(
            expected,
            outputs.get("evidence"),
        )
    )

    evaluation["email_score"] = (
        evaluate_email(
            expected,
            outputs.get("email"),
        )
    )

    valid_scores = [
        score
        for score in evaluation.values()
        if score is not None
    ]

    if valid_scores:

        evaluation["overall_score"] = (
            sum(valid_scores) / len(valid_scores)
        )

    else:

        evaluation["overall_score"] = 0.0

    return evaluation


def main():

    print("=" * 70)
    print("COLD MAIL AGENT — EVALUATOR")
    print("=" * 70)

    cases = load_json(DATASET_PATH)
    results = load_json(RESULTS_PATH)

    results_by_id = {
        result["case_id"]: result
        for result in results
    }

    report = []

    for case in cases:

        case_id = case["case_id"]

        print(
            f"\nEvaluating {case_id}..."
        )

        result = results_by_id.get(
            case_id
        )

        if not result:

            print(
                f"⚠ No result found for {case_id}"
            )

            report.append(
                {
                    "case_id": case_id,
                    "status": "missing",
                }
            )

            continue

        if result.get("status") != "success":

            report.append(
                {
                    "case_id": case_id,
                    "status": "failed",
                    "error": result.get("error"),
                }
            )

            continue

        scores = evaluate_case(
            case,
            result,
        )

        report.append(
            {
                "case_id": case_id,
                "status": "evaluated",
                "scores": scores,
            }
        )

        print(
            f"Overall score: "
            f"{scores['overall_score']:.2%}"
        )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False,
        )

    # ==================================================
    # SUMMARY
    # ==================================================

    evaluated = [
        item
        for item in report
        if item.get("status") == "evaluated"
    ]

    if evaluated:

        overall_scores = [
            item["scores"]["overall_score"]
            for item in evaluated
        ]

        average_score = (
            sum(overall_scores)
            / len(overall_scores)
        )

        print("\n" + "=" * 70)
        print("EVALUATION SUMMARY")
        print("=" * 70)

        print(
            f"Cases evaluated: {len(evaluated)}"
        )

        print(
            f"Average score: {average_score:.2%}"
        )

        print(
            f"\nReport saved to:\n{REPORT_PATH}"
        )


if __name__ == "__main__":
    main()