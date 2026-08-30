# Cold Mail Agent — Product Requirements Document

## 1. Product Overview

### Product Name
Cold Mail Agent

### Product Type
AI-powered job-search outreach assistant

### Product Vision

Enable job seekers to identify relevant recruiters for a specific job opportunity and generate evidence-backed, personalized cold outreach with minimal manual research.

### Product Goal

Reduce the time and effort required to:

1. Understand a target job opportunity
2. Identify relevant recruiters
3. Prioritize recruiters based on job relevance
4. Find a professional email address
5. Identify relevant connections between the candidate's experience and the target role
6. Generate personalized outreach
7. Review and approve the outreach before sending

The product is designed as an **AI-assisted workflow**, not a fully autonomous outreach system.

---

# 2. Problem Statement

Job seekers often use direct recruiter outreach to increase their chances of getting noticed during a job search.

However, preparing effective outreach requires significant manual research.

A candidate typically needs to:

- Read and understand the job description
- Determine what type of recruiter is relevant
- Search for recruiters at the target company
- Evaluate whether each recruiter is relevant
- Consider geographic relevance
- Find a professional email address
- Review their own experience for relevant talking points
- Write and personalize the outreach message

This process is fragmented across search engines, recruiting platforms, email-finding tools, and document editors.

### Problem

Candidates lack a single workflow that connects:

**Job understanding → Recruiter discovery → Recruiter prioritization → Contact discovery → Evidence matching → Personalized outreach**

### Opportunity

An AI-assisted product can combine these activities into a single workflow while maintaining human control over the final outreach.

---

# 3. Target User

## Primary User

Job seekers who:

- Apply to professional positions
- Use cold outreach as part of their job search
- Have a resume available
- Have a target job description
- Want to contact recruiters directly
- Want to reduce manual recruiter research

## Initial Target Segment

Graduate students, early-career professionals, and experienced professionals applying to:

- Data Science
- Machine Learning
- Artificial Intelligence
- Data Analytics
- Product Management
- Software/Technology
- Consulting

roles.

---

# 4. Jobs To Be Done

### Primary Job

"When I find a job I want, help me identify relevant recruiters and prepare a personalized outreach email without requiring me to manually research every recruiter and write the message from scratch."

### Supporting Jobs

The product should help the user:

- Understand important job requirements
- Identify relevant recruiting functions
- Discover recruiters associated with the target company
- Prioritize recruiters based on relevance
- Consider geographic relevance
- Find professional contact information
- Identify relevant candidate experience
- Generate personalized outreach
- Verify that generated claims are supported by available evidence
- Review and approve outreach before sending

---

# 5. Current MVP

The current repository implements the following workflow:

**Job Description + Resume**

↓

**JD & Resume Analysis**

↓

**Recruiter Discovery**

↓

**Recruiter Ranking**

↓

**User Selects Recruiter**

↓

**Hunter Email Lookup**

↓

**Evidence Matching**

↓

**Personalized Email**

The current implementation uses Python, Streamlit, Google Gemini, Hunter API, DuckDuckGo/DDGS, Pydantic, and Pytest. The repository currently contains separate application, configuration, data, and testing components.

### Current MVP Capabilities

- Job description analysis
- Resume analysis
- Recruiter discovery through web search
- Recruiter prioritization
- Role/location-based ranking
- User recruiter selection
- Hunter-based email lookup
- Candidate-to-job evidence matching
- Personalized email generation

---

# 6. Product Goals

## G1 — Reduce Manual Research

Reduce the amount of manual effort required to identify and research relevant recruiters.

## G2 — Improve Recruiter Relevance

Prioritize recruiters based primarily on their relevance to the target job and company.

## G3 — Improve Outreach Personalization

Generate outreach using evidence from:

- Job description
- Candidate resume
- Recruiter information

## G4 — Preserve Human Control

The user must remain responsible for approving outreach before it is sent.

## G5 — Make AI Decisions Explainable

Users should understand why a recruiter was recommended and what evidence was used to personalize the email.

## G6 — Operate Reliably

The system must handle:

- Missing information
- Search failures
- API failures
- API quotas
- Invalid AI output
- Missing email addresses
- Weak recruiter evidence

without silently producing incorrect results.

---

# 7. Non-Goals

The MVP will not:

- Automatically apply to jobs
- Automatically send emails without approval
- Guarantee recruiter responses
- Guarantee interviews
- Replace LinkedIn or recruiting platforms
- Automatically determine whether a recruiter will hire the candidate
- Maximize outreach volume
- Train a custom LLM
- Build an autonomous job-search system
- Use unauthorized automated access to third-party platforms
- Optimize recruiter ranking using machine learning before sufficient feedback data exists

The product prioritizes:

**Relevance > volume**

and

**Quality > autonomy**

---

# 8. Core User Journey

## Step 1 — Provide Job Description

The user uploads or provides a job description.

## Step 2 — Provide Resume

The user provides their resume.

## Step 3 — Analyze Opportunity

The system extracts relevant information including:

- Company
- Role
- Location
- Required skills
- Preferred skills
- Responsibilities
- Relevant recruiting functions

## Step 4 — Discover Recruiters

The system uses web search to identify potentially relevant recruiters.

The MVP uses DuckDuckGo/DDGS for this discovery process.

## Step 5 — Rank Recruiters

The system scores recruiters using predefined relevance signals.

## Step 6 — Explain Recommendations

The system displays:

- Recruiter
- Company
- Role/title
- Location when available
- Relevance score
- Key ranking signals
- Supporting evidence

## Step 7 — User Selects Recruiter

The user chooses the recruiter they want to contact.

## Step 8 — Email Discovery

The system attempts to identify a professional email using Hunter.

## Step 9 — Evidence Matching

The system identifies relevant connections between:

**Candidate experience ↔ Job requirements**

## Step 10 — Email Generation

The system generates personalized outreach.

## Step 11 — Claim Verification

The system checks factual claims in the generated email against available candidate and recruiter evidence.

## Step 12 — Human Review

The user reviews and edits the message.

## Step 13 — Approval

The user explicitly approves the final outreach.

---

# 9. Recruiter Discovery

## Product Requirement

The system must identify publicly discoverable recruiters who are potentially relevant to the target job and company.

### MVP Data Source

The current MVP uses DuckDuckGo/DDGS web search for recruiter discovery. DuckDuckGo states that its traditional search results include links largely sourced from Bing along with other sources and its own indexes.

### Important Product Constraint

The product should distinguish between:

**Using a search engine to discover publicly indexed information**

and

**Directly scraping or automating interaction with a third-party platform.**

The MVP should not directly automate interaction with LinkedIn.

The product should not represent the DuckDuckGo discovery mechanism as a LinkedIn integration.

### Production Requirement

Before production deployment, the data-acquisition approach must be reviewed against the applicable terms and restrictions of external search and data providers.

The product must use permitted:

- Search APIs/services
- Licensed data providers
- Publicly accessible information where permitted
- User-provided information

The product must not depend on unauthorized automated access to third-party platforms.

---

# 10. Recruiter Ranking

Recruiter ranking is a core product capability.

## Ranking Principle

**Recruiter relevance > geographic proximity**

Location should influence ranking but should not override strong functional relevance.

### Initial Ranking Signals

| Signal | Priority |
|---|---|
| Target company match | High |
| Recruiting-function relevance | High |
| Job/skill relevance | High |
| Evidence quality | High |
| Geographic relevance | Medium |
| Recruiter title/seniority relevance | Medium |

### Example

For:

**Data Scientist — Microsoft — Dallas**

A recruiter who:

- Works at Microsoft
- Recruits Data/AI roles
- Is located in Austin

should potentially rank above a:

- Microsoft recruiter
- Located in Dallas
- Recruiting unrelated functions

### Geographic Fallback

If insufficient relevant recruiters are identified in the target location:

1. Expand discovery to other locations.
2. Preserve company relevance.
3. Preserve recruiting-function relevance.
4. Inform the user that geographic fallback was applied.

The system should never select an irrelevant recruiter solely because they are geographically closer.

---

# 11. Recruiter Recommendation

Each recommendation should provide:

- Recruiter name
- Company
- Job title
- Location when available
- Relevance score
- Ranking signals
- Supporting evidence
- Source information when available

### Explainability Requirement

The user should be able to answer:

> "Why was this recruiter recommended?"

For example:

**Score: 86**

- Company match: +30
- Function match: +30
- Geographic match: +15
- Evidence quality: +11

The exact weighting should be configurable and documented.

The initial scoring framework is a **product hypothesis**, not a learned ranking model.

---

# 12. Email Discovery

The MVP uses Hunter for professional email discovery.

Hunter's current API documentation states that the Email Finder endpoint can find an email using information such as name and domain and costs one credit per email found. Hunter also documents endpoint-specific API rate limits.

## Requirements

The system must:

- Attempt email lookup only after the user selects a recruiter
- Avoid unnecessary repeated lookups
- Cache successful results where appropriate
- Track email lookup usage
- Handle API errors explicitly
- Detect quota exhaustion
- Detect rate limiting
- Never fabricate an email address

### API Cost/Quota Handling

The product should track:

- Number of Hunter lookups
- Successful lookups
- Failed lookups
- Credits consumed
- Remaining available credits when available
- Rate-limit errors
- Quota errors

Hunter currently provides 50 monthly credits on its free All-in-One plan, while paid plans provide higher allocations. Email Finder uses one credit per email found.

### Rate Limits

Hunter currently documents:

- Email Finder: 15 requests/second and 500 requests/minute
- Email Verifier: 10 requests/second and 300 requests/minute

Rate-limit violations result in a 403 response, while exhausted credits can produce a 429 usage-limit response.

### Failure Strategy

If Hunter cannot provide an email:

The system should:

1. Clearly communicate that an email could not be retrieved.
2. Preserve the recruiter recommendation.
3. Allow the user to continue without an email.
4. Avoid fabricating or guessing an email.
5. Provide an alternative contact workflow where available.

### Provider Abstraction

Hunter should be treated as the initial email-discovery provider rather than an inseparable component of the product.

The email-discovery layer should eventually support additional permitted providers without requiring redesign of the rest of the application.

---

# 13. Evidence Matching

The system should identify relevant connections between:

**Candidate experience**

and

**Job requirements**

Examples:

- Candidate skill ↔ required skill
- Candidate project ↔ job responsibility
- Candidate experience ↔ required qualification
- Candidate industry experience ↔ target role

Personalization must be grounded in available evidence.

---

# 14. Claim Traceability

Prompt instructions alone are insufficient to guarantee that generated emails do not contain fabricated information.

Therefore, generated outreach should pass through a claim-verification step.

## Process

**Resume**

↓

**Structured candidate facts**

↓

**Job description**

↓

**Structured job requirements**

↓

**Evidence matching**

↓

**Email generation**

↓

**Claim extraction**

↓

**Claim verification**

↓

**Human approval**

### Claim Status

Each factual claim should be classified as:

- Verified
- Unsupported
- Uncertain

### Example

**Generated claim:**

> "I recently built a machine learning forecasting model."

**Source:**

Candidate resume → Project/Experience section

**Status:**

Verified

If the system cannot identify supporting evidence, the claim should be removed or regenerated.

### Requirement

The system must prefer:

**Unknown / unsupported**

over fabricated information.

---

# 15. Email Generation

Generated outreach should:

- Address the recruiter appropriately
- Reference the target company
- Reference the target position
- Connect candidate experience to the opportunity
- Remain concise
- Use professional language
- Avoid generic filler
- Avoid unsupported claims
- Avoid fabricated recruiter information
- Remain editable by the user

The system should prioritize **specific evidence-backed personalization** rather than simply inserting the recruiter's name and company.

---

# 16. Human-in-the-Loop

The user must remain in control of outreach.

The user should be able to:

- Review recruiter recommendations
- Select or reject recruiters
- Review recruiter evidence
- Review email information
- Edit generated emails
- Regenerate emails
- Review claim verification
- Approve the final email

The product must not automatically send outreach without explicit user approval.

---

# 17. Reliability & Failure Handling

| Failure | Product Behavior |
|---|---|
| No recruiters found | Broaden search strategy |
| Few local recruiters | Apply geographic fallback |
| Weak recruiter evidence | Lower confidence or exclude |
| Duplicate recruiter | Deduplicate |
| Search failure | Retry or return controlled failure |
| Hunter email unavailable | Continue without email |
| Hunter quota exhausted | Inform user and preserve workflow |
| Hunter rate limited | Delay/retry according to provider constraints |
| Invalid email | Do not present as verified |
| LLM output invalid | Validate and regenerate |
| Missing resume evidence | Do not fabricate |
| Unsupported email claim | Remove/regenerate |
| Missing recruiter information | Mark as unknown |
| External source unavailable | Use available permitted alternatives |

The system should never silently convert missing information into assumptions.

---

# 18. Data Persistence

The current MVP should evolve from a single-session workflow toward persistent job-search campaigns.

## Product Requirement

Users should eventually be able to retain:

- Jobs
- Recruiters
- Recruiter scores
- Evidence
- Generated emails
- Outreach status
- User feedback

### Proposed Data Model

**User**

↓

**Campaign**

↓

**Job**

↓

**Recruiter**

↓

**Contact**

↓

**Generated Email**

↓

**Outreach Status**

### Minimum Persistence Requirements

The system should eventually track:

- Company
- Job title
- Job URL when available
- Recruiter
- Recruiter company
- Recruiter ranking
- Email
- Email generation timestamp
- Approval status
- Outreach status
- Contact history

### Product Reason

Persistence prevents:

- Duplicate outreach
- Repeated research
- Loss of previous campaigns
- Inability to track outcomes

SQLite is sufficient for the initial productized version. A production database can be introduced later based on usage requirements.

---

# 19. Product Analytics & Event Tracking

The system should begin collecting product events before building a sophisticated analytics dashboard.

## Core Events

| Event | Example Data |
|---|---|
| JD submitted | Role/company/location |
| Resume submitted | Resume ID |
| Recruiter search started | Job ID |
| Recruiters discovered | Number discovered |
| Fallback triggered | Reason |
| Recruiter selected | Recruiter/rank |
| Recruiter rejected | Reason |
| Email lookup requested | Recruiter |
| Email found | Yes/No |
| Email generated | Yes/No |
| Email edited | Yes/No |
| Email regenerated | Yes/No |
| Email approved | Yes/No |
| Email sent | Yes/No |
| Recruiter feedback | Relevant/Not relevant |

This data will eventually support product decisions and evaluation.

---

# 20. Success Metrics

Because the MVP currently has no meaningful real-world usage dataset, initial metrics should be treated as **product hypotheses**, not claimed performance results.

## Discovery Metrics

- Jobs processed
- Recruiter searches completed
- Recruiters discovered per job
- Search success rate
- Fallback frequency

## Recruiter Quality Metrics

- Company-match rate
- Function-match rate
- Geographic-match rate
- Evidence coverage
- Recruiter rejection rate

## Email Metrics

- Email lookup success rate
- Email generation success rate
- Email regeneration rate
- Email edit rate
- Unsupported-claim rate
- Claim verification rate

## Operational Metrics

- Hunter credits consumed per successful contact
- Hunter failure rate
- API rate-limit frequency
- LLM failure rate
- Average processing time
- Cost per completed outreach draft

## Outcome Metrics

Once sufficient real outreach data exists:

- Email response rate
- Positive response rate
- Recruiter engagement rate
- Interview conversion rate

These metrics should not be claimed until actual user/outreach data exists.

---

# 21. Initial AI Evaluation Strategy

The product currently has no labeled recruiter dataset.

Therefore, the first evaluation phase should **not** attempt to measure whether the AI selected the exact recruiter a human would select.

Instead, evaluation should measure whether the system behaves according to explicit product requirements.

## Evaluation Dataset

Create a controlled set of representative job scenarios.

The dataset should cover:

- Different companies
- Different roles
- Different locations
- Different recruiting functions
- Cases with strong local recruiters
- Cases requiring geographic fallback
- Cases with irrelevant local recruiters
- Cases with limited recruiter information
- Cases where no suitable recruiter can be identified

## Evaluation Criteria

For each scenario, evaluate whether the system:

1. Correctly identifies the company
2. Correctly identifies the target role/function
3. Prioritizes relevant recruiting functions
4. Uses geography appropriately
5. Applies fallback appropriately
6. Provides supporting evidence
7. Avoids unsupported claims
8. Handles unavailable information correctly

### Initial Evaluation Metric

Use a **requirement pass rate**:

> Number of product requirements satisfied / Number of requirements tested

This is a behavioral evaluation rather than a ground-truth ranking evaluation.

---

# 22. Recruiter Ranking Ground Truth

A formal recruiter-ranking ground truth does not currently exist.

Therefore, the product should not claim:

> "The AI ranks recruiters accurately."

Instead:

### Phase 1

Evaluate ranking behavior against predefined product rules.

### Phase 2

Collect lightweight user feedback.

For example:

> **Was this recruiter relevant?**

- Yes
- No

If No:

- Wrong company
- Wrong function
- Wrong location
- Insufficient evidence
- Other

### Phase 3

Use accumulated feedback to create a labeled dataset.

### Phase 4

Evaluate ranking performance using metrics such as:

- Precision@K
- Recall@K
- NDCG@K
- Recruiter acceptance rate

Only after sufficient labeled data exists should formal ranking experiments be performed.

---

# 23. AI Reliability Evaluation

Email generation should be evaluated separately from recruiter discovery.

## Email Evaluation Criteria

Each generated email should be checked for:

- Correct recruiter
- Correct company
- Correct role
- Correct candidate information
- Relevant personalization
- Evidence-backed claims
- Professional tone
- Appropriate length
- Absence of fabricated information

### Evaluation Methods

Use deterministic checks where possible for:

- Names
- Company
- Job title
- Candidate experience
- Unsupported facts
- Length

Use model-based evaluation only for subjective dimensions such as:

- Relevance
- Personalization quality
- Tone

LLM-based evaluation should not be treated as the sole source of truth.

---

# 24. Product Feedback Loop

The product should eventually create a continuous improvement loop:

**Agent Recommendation**

↓

**User Decision**

↓

**Feedback**

↓

**Evaluation Dataset**

↓

**Ranking/Prompt/Product Improvement**

↓

**New Version**

Initially, the feedback system should collect information rather than automatically retrain models.

The goal is to understand where the agent fails before introducing learning-to-rank or fine-tuning.

---

# 25. External Dependencies & Operational Constraints

| Dependency | Purpose | Risk | Mitigation |
|---|---|---|---|
| Gemini/LLM | Analysis & generation | Cost, failure, invalid output | Structured outputs, validation, retries |
| DuckDuckGo/DDGS | Recruiter discovery | Search quality, availability, provider restrictions | Search abstraction, fallback strategy |
| Hunter | Email discovery | Credits, quota, rate limits | Caching, usage tracking, provider abstraction |
| External web sources | Recruiter evidence | Stale/incomplete information | Source tracking, confidence |
| Streamlit | MVP interface | Limited production scalability | Replace/extend UI if usage requires |

### Data Source Policy

The product must not assume that information returned through a search engine can automatically be scraped or reused without restriction.

For production deployment, each external data source must be reviewed for:

- Terms of service
- API usage restrictions
- Automated access restrictions
- Data licensing
- Privacy requirements

The MVP's use of DuckDuckGo/DDGS is a **search-based discovery mechanism**, not a LinkedIn scraping system.

---

# 26. Cost Management

The product should track major variable costs.

## LLM Cost

Track:

- Input tokens
- Output tokens
- Model
- Cost per workflow

## Hunter Cost

Track:

- Lookup requests
- Successful email discoveries
- Credits consumed
- Cost per successful email

## Search Cost

Track:

- Search requests
- Queries per job
- Results returned
- Search failures

### Product Metric

A useful eventual metric is:

> **Cost per completed outreach draft**

This allows future decisions about model selection, caching, and provider usage.

---

# 27. Product Hypotheses

### H1 — Recruiter Relevance

Users prefer recruiters whose recruiting function is closely aligned with the target role.

### H2 — Geographic Relevance

Geographic relevance improves usefulness but should not override functional relevance.

### H3 — Explainability

Users are more likely to trust recruiter recommendations when the system explains why they were selected.

### H4 — Evidence-Based Personalization

Outreach based on specific candidate/job evidence requires less manual editing than generic generated outreach.

### H5 — Human Approval

Users prefer reviewing outreach before sending rather than allowing completely autonomous outreach.

### H6 — Persistence

Users benefit from retaining recruiter and outreach history across multiple job applications.

These hypotheses should be validated through actual usage rather than assumed to be true.

---

# 28. Experimentation Strategy

Formal A/B experiments should **not** be the immediate evaluation mechanism because the product does not yet have sufficient labeled recruiter data or user volume.

## Current Stage

Use:

- Controlled test cases
- Requirement pass rates
- Failure analysis
- Claim verification
- API reliability metrics
- Manual inspection of edge cases

## Future Stage

Once sufficient user feedback exists:

### Ranking Experiment

Compare alternative ranking strategies such as:

- Relevance-only
- Relevance + geographic signal
- Relevance + geography + evidence quality

Evaluate using:

- Recruiter acceptance rate
- Recruiter rejection rate
- Precision@K
- Recall@K
- NDCG@K

### Email Experiment

Compare:

- Generic role-based personalization
- JD + resume evidence-based personalization

Evaluate using:

- Edit rate
- Regeneration rate
- Approval rate

Eventually:

- Response rate
- Positive response rate

---

# 29. Product Roadmap

## Phase 1 — MVP

### Completed

- JD analysis
- Resume analysis
- Recruiter discovery
- Recruiter ranking
- Location-based prioritization
- User recruiter selection
- Hunter email lookup
- Evidence matching
- Personalized email generation

---

## Phase 2 — Productization

### Priority

- Formal recruiter ranking specification
- Ranking explanations
- Evidence/source display
- Failure-state handling
- Hunter usage tracking
- Hunter result caching
- API error handling
- User feedback
- Basic persistence
- Event tracking
- Duplicate outreach prevention

---

## Phase 3 — AI Evaluation

### Priority

- Controlled evaluation dataset
- Requirement-based evaluation
- Ranking behavior tests
- Email quality evaluation
- Claim verification
- Hallucination/unsupported-claim testing
- Edge-case testing

---

## Phase 4 — Product Analytics

### Priority

- Workflow funnel
- Recruiter discovery metrics
- Ranking metrics
- Email quality metrics
- API cost metrics
- Failure metrics
- User feedback analytics

---

## Phase 5 — Real-World Validation

### Priority

- Recruiter relevance feedback
- Email quality feedback
- Outreach history
- Response tracking
- Ranking evaluation dataset
- Formal ranking experiments

---

## Phase 6 — Production

### Potential Capabilities

- Authentication
- Production database
- Scalable deployment
- Monitoring
- Secrets management
- Cost controls
- Provider abstraction
- Production-grade data-source integrations

---

# 30. Future Features

Potential future capabilities include:

- Gmail integration
- Outlook integration
- Outreach scheduling
- Follow-up generation
- Response classification
- Campaign management
- Multi-job campaigns
- Outreach analytics
- Recruiter relationship history
- Additional permitted recruiter-data providers
- Learning-to-rank
- Personalized outreach strategies
- Semi-autonomous follow-up workflows

These are intentionally outside the initial product scope.

---

# 31. Product Principles

## Relevance Over Volume

The product should identify useful contacts rather than maximize outreach volume.

## Evidence Over Assumptions

The system should use verifiable information whenever possible.

## Human Control Over Autonomy

The user must approve outreach before sending.

## Quality Over Automation

Automating an incorrect recommendation creates more harm than requiring user review.

## Progressive Autonomy

The product should become more autonomous only after reliability is demonstrated.

## Graceful Degradation

External API failure or missing information should reduce functionality rather than cause the entire workflow to fail.

## Transparency

The product should clearly communicate:

- Why a recruiter was recommended
- What evidence was used
- When information is uncertain
- When an external service fails
- When a fallback strategy was applied

---

# 32. Definition of Success

The product will be considered successful when a user can:

1. Provide a job description and resume.
2. Receive relevant recruiter recommendations.
3. Understand why recruiters were recommended.
4. Select a recruiter.
5. Obtain a professional email when available.
6. Understand how their experience relates to the target role.
7. Receive a personalized outreach draft.
8. Verify that factual claims are supported by evidence.
9. Edit and approve the final message.
10. Preserve the campaign and outreach history.
11. Complete the workflow with substantially less manual research than the traditional process.

The initial product objective is **not to prove that AI generates more recruiter responses than a human**.

The initial objective is to demonstrate that AI can reliably reduce the manual research and personalization burden involved in recruiter outreach while maintaining user control, evidence traceability, and operational reliability.

---

# 33. Key Product Decisions

The following decisions should be explicitly maintained as part of the product decision log.

### Decision 1 — Relevance Over Location

**Decision:** Recruiter relevance takes precedence over geographic proximity.

**Reason:** A functionally relevant recruiter outside the target city may be more valuable than an irrelevant recruiter in the target city.

**Tradeoff:** Some highly relevant recruiters may be outside the user's preferred location.

---

### Decision 2 — Geographic Fallback

**Decision:** If insufficient relevant recruiters exist in the target city, expand to other locations within the target company.

**Reason:** A hard geographic filter can unnecessarily eliminate relevant recruiters.

---

### Decision 3 — Human Approval

**Decision:** Outreach requires explicit user approval.

**Reason:** Incorrect personalization or fabricated information could damage the user's professional reputation.

---

### Decision 4 — Evidence-Based Personalization

**Decision:** Generated factual claims must be traceable to source evidence.

**Reason:** Prompt instructions alone do not provide sufficient protection against hallucination.

---

### Decision 5 — Requirement-Based Evaluation Before Ranking Ground Truth

**Decision:** Initial evaluation will test compliance with predefined product requirements rather than claiming a ground-truth recruiter ranking.

**Reason:** The product currently lacks sufficient labeled recruiter data.

---

### Decision 6 — DuckDuckGo-Based Discovery for MVP

**Decision:** Use DuckDuckGo/DDGS as the initial recruiter discovery mechanism.

**Reason:** It allows the MVP to discover publicly indexed information without building a direct LinkedIn automation/scraping system.

**Production consideration:** External search/data-source terms and permitted use must be reviewed before production deployment.

---

### Decision 7 — Hunter as Replaceable Provider

**Decision:** Hunter is the initial email-discovery provider but should remain behind a provider abstraction.

**Reason:** API credits, pricing, rate limits, and availability create operational dependency.

---

### Decision 8 — Persistence Before Full Production

**Decision:** Basic campaign persistence should be introduced during productization rather than waiting for the final production phase.

**Reason:** Job seekers are expected to use the product across multiple applications, making outreach history and duplicate prevention important product capabilities.

---

# 34. Product Development Loop

The intended product development loop is:

**PRD**

↓

**Product Requirements**

↓

**Controlled Evaluation**

↓

**MVP Improvements**

↓

**User Feedback**

↓

**Product Analytics**

↓

**Real-World Dataset**

↓

**Experiments**

↓

**Product Iteration**

↓

**Next Product Version**

The product should not introduce advanced autonomy, machine-learning ranking, or large-scale experimentation before sufficient evidence exists to justify those capabilities.