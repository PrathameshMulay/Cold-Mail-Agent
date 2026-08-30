# AI Recruiter Agent
## AI Evaluation & Experiment Plan

# 1. Evaluation Objective

The product should be evaluated on whether it produces **useful, accurate recruiter outreach**, not merely whether the AI generates plausible text.

The evaluation framework therefore measures:

1. Discovery quality
2. Ranking quality
3. Evidence quality
4. Personalization quality
5. Workflow efficiency
6. Cost and reliability

---

# 2. Evaluation Principle

The PRD defines the product requirements first.

Evaluation then determines whether the implementation satisfies those requirements.

```text
Requirement
    ↓
Acceptance criterion
    ↓
Test case
    ↓
Metric
    ↓
Result
    ↓
Product decision
```

---

# 3. Experiment 1 — Recruiter Discovery

### Hypothesis

The agent can identify recruiters relevant to a target job using public web search.

### Method

Create a labeled dataset of jobs and manually identify recruiters considered relevant.

Run the agent on the same jobs.

Compare agent results against human judgments.

### Metrics

**Precision**

Relevant recruiters / recruiters returned.

**Recall**

Relevant recruiters found / relevant recruiters in labeled set.

### Target

The initial target should prioritize precision over maximum recall because contacting an irrelevant recruiter can create a poor user experience.

---

# 4. Experiment 2 — Recruiter Ranking

### Hypothesis

The ranking system places the most relevant recruiters near the top.

### Method

For each job, ask human evaluators to rank discovered recruiters.

Compare human rankings against system rankings.

### Metrics

- Precision@K
- Recall@K
- NDCG@K
- Top-1 relevance
- Top-3 relevance

### Product decision

If the top-ranked recruiters are frequently irrelevant, improve ranking signals before expanding discovery volume.

---

# 5. Experiment 3 — Personalization Accuracy

### Hypothesis

The AI can generate personalized outreach without introducing unsupported claims.

### Evaluation dimensions

Each message is evaluated for:

| Dimension | Question |
|---|---|
| Accuracy | Are factual claims correct? |
| Evidence | Can claims be traced to evidence? |
| Relevance | Does the message relate to the target role? |
| Personalization | Is the message meaningfully customized? |
| Professionalism | Is the tone appropriate? |
| Clarity | Is the message concise and understandable? |

Use a 1–5 human rating scale.

---

# 6. Hallucination / Unsupported Claim Test

For every generated email:

1. Extract factual claims.
2. Identify the source evidence.
3. Determine whether the evidence actually supports the claim.

Metric:

> Unsupported claim rate = unsupported claims / total factual claims

The desired direction is toward zero unsupported claims.

---

# 7. Experiment 4 — Human Editing

### Hypothesis

The AI-generated message should require limited editing.

Track:

- Percentage of messages approved without edits
- Average number of edits
- Regeneration rate
- Rejection rate

A high rejection/edit rate indicates that personalization or tone needs improvement.

---

# 8. Experiment 5 — Time Savings

### Hypothesis

The product reduces the time required to produce qualified recruiter outreach.

Compare:

### Baseline

Manual workflow.

### Treatment

AI recruiter agent.

Measure:

- Time to discover recruiter
- Time to verify recruiter
- Time to find contact
- Time to draft message
- Total time per outreach

Primary metric:

> Total time to produce a qualified outreach opportunity.

---

# 9. Experiment 6 — Contact Enrichment

Measure:

- Lookup success rate
- Valid email rate
- Quota usage
- Duplicate lookup rate
- Cost per successful enrichment

The system should optimize for useful results rather than maximum API usage.

---

# 10. Experiment 7 — End-to-End Workflow

Evaluate the complete journey:

```text
JD
 ↓
Candidate analysis
 ↓
Recruiter discovery
 ↓
Ranking
 ↓
Enrichment
 ↓
Evidence
 ↓
Email
 ↓
Approval
```

Measure the percentage of workflows that successfully reach each stage.

This creates a funnel:

| Stage | Success |
|---|---:|
| JD analyzed | TBD |
| Recruiters discovered | TBD |
| Relevant recruiter found | TBD |
| Contact enriched | TBD |
| Email generated | TBD |
| Email approved | TBD |
| Email sent | TBD |

---

# 11. Cost Evaluation

Track:

- LLM tokens
- LLM cost
- Search requests
- Enrichment requests
- Enrichment cost
- Infrastructure cost

Calculate:

> Cost per qualified outreach opportunity.

This metric is important if the product eventually scales.

---

# 12. Evaluation Dataset

A formal evaluation dataset should contain:

- Job description
- Company
- Target function
- Candidate profile
- Candidate recruiters
- Human relevance labels
- Evidence
- Expected personalization facts

The dataset should be version-controlled so that model or ranking changes can be compared consistently.

---

# 13. Decision Rules

### If discovery precision is low

Improve search queries and recruiter filtering.

### If ranking is weak

Improve ranking signals.

### If personalization is inaccurate

Strengthen evidence extraction and claim verification.

### If emails require extensive editing

Improve prompts and personalization logic.

### If enrichment is expensive

Improve caching and provider strategy.

### If users save little time

Reconsider which parts of the workflow should be automated.

---

# 14. Evaluation Outcome

The product should only be considered validated when quantitative and qualitative evidence demonstrate that it:

1. Finds relevant recruiters.
2. Ranks useful candidates near the top.
3. Generates accurate personalization.
4. Reduces manual effort.
5. Provides sufficient transparency for users to trust recommendations.