# AI Recruiter Agent
## User Stories & Acceptance Criteria

# Epic 1 — Job Analysis

### US-01 — Submit Job Description

**As a job seeker, I want to provide a job description so that the system can understand the opportunity.**

Acceptance criteria:

- [ ] User can submit a job description.
- [ ] Empty input is rejected.
- [ ] Valid input initiates analysis.
- [ ] Processing failures produce an understandable error.

---

### US-02 — Extract Job Requirements

**As a job seeker, I want the system to identify important job requirements so that recruiter matching can use them.**

Acceptance criteria:

- [ ] Role is identified.
- [ ] Company is identified where available.
- [ ] Required skills are extracted.
- [ ] Functional area is identified where possible.
- [ ] Seniority is identified where possible.
- [ ] Output follows a validated schema.

---

# Epic 2 — Candidate Analysis

### US-03 — Analyze Candidate Profile

**As a job seeker, I want the system to understand my experience so that recruiters can be evaluated against my target role.**

Acceptance criteria:

- [ ] Skills are extracted.
- [ ] Relevant experience is extracted.
- [ ] Education is extracted.
- [ ] Relevant projects can be identified.
- [ ] Output is stored for downstream processing.

---

# Epic 3 — Recruiter Discovery

### US-04 — Discover Recruiters

**As a job seeker, I want the system to find potentially relevant recruiters so that I do not have to manually search for them.**

Acceptance criteria:

- [ ] Search is based on company and role/function context.
- [ ] Public web search is used for discovery.
- [ ] Duplicate results are removed.
- [ ] Recruiter information is stored in structured form.
- [ ] Source information is retained where available.

---

# Epic 4 — Recruiter Ranking

### US-05 — Rank Recruiters

**As a job seeker, I want recruiters ranked by relevance so that I can focus on the strongest outreach opportunities.**

Acceptance criteria:

- [ ] Company relevance is considered.
- [ ] Functional relevance is considered.
- [ ] Role relevance is considered.
- [ ] Evidence strength is considered.
- [ ] Ranking output is deterministic/reproducible where possible.
- [ ] The system explains why a recruiter received a high ranking.

---

# Epic 5 — Contact Enrichment

### US-06 — Enrich Recruiter Contact

**As a job seeker, I want contact information retrieved for a selected recruiter so that I can reach out.**

Acceptance criteria:

- [ ] User selects recruiter before enrichment.
- [ ] Enrichment provider is called only when necessary.
- [ ] Results are cached where appropriate.
- [ ] Provider failures are handled gracefully.
- [ ] Usage is tracked.
- [ ] Quota exhaustion does not crash the workflow.

---

# Epic 6 — Evidence

### US-07 — Verify Personalization Evidence

**As a job seeker, I want to see the evidence behind recruiter recommendations and personalized claims so that I can trust the generated message.**

Acceptance criteria:

- [ ] Evidence is stored with the recruiter.
- [ ] Generated claims can be mapped to evidence.
- [ ] Unsupported claims are rejected or flagged.
- [ ] User can inspect evidence before sending.

---

# Epic 7 — Outreach Generation

### US-08 — Generate Personalized Outreach

**As a job seeker, I want an email generated from my profile, the job, recruiter information, and evidence so that I do not have to write every message manually.**

Acceptance criteria:

- [ ] Candidate context is included.
- [ ] Job context is included.
- [ ] Recruiter context is included.
- [ ] Only supported evidence is used.
- [ ] Output follows the expected email schema.
- [ ] Email is readable and professional.

---

# Epic 8 — Human Approval

### US-09 — Review Email

**As a job seeker, I want to review the generated message before sending it so that I retain control over my outreach.**

Acceptance criteria:

- [ ] User can view the complete message.
- [ ] User can edit it.
- [ ] User can regenerate it.
- [ ] User can reject it.
- [ ] Sending requires explicit approval.

---

# Epic 9 — Sending

### US-10 — Send Approved Email

**As a job seeker, I want to send an approved email so that I can complete the outreach workflow.**

Acceptance criteria:

- [ ] Only approved messages can be sent.
- [ ] Sending status is recorded.
- [ ] Failures are surfaced to the user.
- [ ] Credentials are securely managed.
- [ ] The system does not expose secrets.

---

# Epic 10 — Persistence

### US-11 — Persist Workflow

**As a user, I want my recruiter and outreach information saved so that I do not repeat the same work.**

Acceptance criteria:

- [ ] Jobs are persisted.
- [ ] Recruiters are persisted.
- [ ] Evidence is persisted.
- [ ] Enrichment results are persisted.
- [ ] Outreach state is persisted.
- [ ] Duplicate records can be detected.

---

# Epic 11 — Observability

### US-12 — Track System Activity

**As a product owner, I want system activity logged so that I can diagnose failures and measure product performance.**

Acceptance criteria:

- [ ] Major workflow steps are logged.
- [ ] External API failures are recorded.
- [ ] Processing errors are recorded.
- [ ] Usage metrics are captured.
- [ ] Logs do not expose sensitive credentials.

---

# MVP Definition of Done

The MVP is considered functionally complete when:

- [ ] Job can be analyzed.
- [ ] Candidate can be analyzed.
- [ ] Recruiters can be discovered.
- [ ] Recruiters can be ranked.
- [ ] User can select a recruiter.
- [ ] Contact enrichment works or gracefully fails.
- [ ] Evidence is available.
- [ ] Personalized outreach can be generated.
- [ ] User can review and edit.
- [ ] User explicitly approves before sending.
- [ ] Workflow state is persisted.
- [ ] Core failures are handled.
- [ ] Core workflow is tested end-to-end.