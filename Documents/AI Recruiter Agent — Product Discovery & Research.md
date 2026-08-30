# AI Recruiter Agent
## Product Discovery & Research

### 1. Discovery Objective

The objective of product discovery was to determine whether recruiter outreach represents a meaningful workflow problem and, if so, which parts of that workflow are appropriate for AI automation.

The initial hypothesis was that job seekers spend significant effort manually identifying recruiters, validating recruiter relevance, finding contact information, and creating personalized outreach.

---

## 2. Target User

The initial target segment is:

> Students and early-career professionals actively applying to competitive roles who want to supplement applications with targeted recruiter outreach.

This segment was selected because the workflow is frequent, repetitive, and highly research-intensive.

---

## 3. Current User Workflow

The existing process generally involves:

1. Identify a target job.
2. Understand the hiring function.
3. Search for recruiters.
4. Evaluate recruiter relevance.
5. Search for contact information.
6. Research the recruiter/company.
7. Write outreach.
8. Review the message.
9. Send it.
10. Track the result.

---

## 4. Pain-Point Hypotheses

### Hypothesis 1 — Recruiter discovery is time-consuming

Users may know the company but not know who is responsible for recruiting for the target role.

### Hypothesis 2 — Relevance is difficult to determine

Finding someone with the title "Recruiter" does not mean that person is responsible for the target function.

### Hypothesis 3 — Contact enrichment creates friction

Even after identifying a relevant recruiter, finding a reliable email address may require another tool or workflow.

### Hypothesis 4 — Personalization is expensive

Users know that generic messages are weak, but researching every recruiter sufficiently to personalize each message is time-consuming.

### Hypothesis 5 — Users do not necessarily want full autonomy

Sending an incorrect or poorly personalized message can damage the user's professional reputation.

Therefore, users may prefer AI assistance with human approval rather than fully autonomous outreach.

---

## 5. Competitive / Alternative Workflow

The user currently has several alternatives:

### Manual search

High control but high time cost.

### LinkedIn-based research

Potentially rich information but dependent on platform workflows and policies.

### Email enrichment tools

Useful for finding contact information but do not solve recruiter discovery or personalization by themselves.

### Generic AI assistants

Can generate emails but generally require the user to manually gather recruiter information and context.

### Proposed product

Combines:

```text
Discovery
+
Ranking
+
Enrichment
+
Evidence
+
Personalization
+
Human approval
```

---

## 6. Product Opportunity

The opportunity is not to replace the user's judgment.

It is to automate repetitive research and provide a decision-ready recommendation.

The desired experience is:

> "Here are the three recruiters most likely to be relevant to this role. Here is why each was selected, what evidence supports the recommendation, the available contact information, and a personalized outreach draft."

---

## 7. Discovery Questions

Future user research should investigate:

### Workflow

- How do users currently identify recruiters?
- How long does recruiter research take?
- How many recruiters do they contact per application?
- At what point do they abandon outreach?

### Relevance

- What makes a recruiter "relevant"?
- How important are recruiting title, function, geography, business unit, and seniority?
- How much evidence does a user need before contacting someone?

### Outreach

- How much personalization is expected?
- How much editing do users perform on AI-generated drafts?
- What makes a user reject a generated email?

### Trust

- What AI errors would make the user stop using the product?
- How important is evidence behind generated claims?
- Would users allow automatic sending?

### Value

- How much time does the product save?
- Does it increase the number of qualified outreach attempts?
- Does it improve response rates?

---

## 8. Research Plan

A structured validation phase should include:

### Qualitative

Conduct interviews with target users and recruiters.

Capture:

- Current workflow
- Pain points
- Workarounds
- Trust concerns
- Decision criteria
- Desired outcomes

### Quantitative

After MVP development, measure:

- Time to identify a recruiter
- Recruiter relevance
- Enrichment success
- Email editing rate
- Approval rate
- Response rate

---

## 9. Research-to-Product Decision Framework

Each research finding should result in a product decision.

Example:

| Finding | Product implication |
|---|---|
| Users distrust generic AI claims | Require evidence-backed personalization |
| Users want control over outreach | Human approval required |
| Recruiter title alone is insufficient | Use multiple relevance signals |
| Contact lookup can fail | Build graceful degradation |
| Users may repeatedly target same companies | Persist recruiter/application history |

---

## 10. Validation Gap

The current product contains strong hypothesis-driven discovery but still requires structured external validation.

The next research milestone is therefore:

> Validate the assumptions with real target users before expanding the product beyond the MVP.