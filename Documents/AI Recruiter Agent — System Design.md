# AI Recruiter Agent
## System Design

# 1. Architecture Overview

The system is designed as a modular AI-assisted workflow.

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Streamlit UI   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Agent / Workflow │
                         │  Orchestration   │
                         └────────┬─────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
      │ JD Analyzer │      │   Recruiter │      │  Candidate  │
      │             │      │  Discovery  │      │   Analyzer  │
      └─────────────┘      └──────┬──────┘      └─────────────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │   Ranker    │
                           └──────┬──────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │   Human     │
                           │  Selection  │
                           └──────┬──────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │  Enrichment │
                           │   Provider  │
                           └──────┬──────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │   Evidence  │
                           │   Layer     │
                           └──────┬──────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │    Email    │
                           │  Generator  │
                           └──────┬──────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │    Human    │
                           │    Review   │
                           └──────┬──────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │ Email / API │
                           └─────────────┘
```

---

# 2. Technology Responsibilities

### Streamlit

Provides the interactive product interface.

### Python

Implements application logic and workflow orchestration.

### LLM

Used for:

- Job analysis
- Candidate analysis
- Matching
- Reasoning
- Email generation

### DDG/DDGS

Used for public web recruiter discovery.

### Hunter

Used for contact enrichment.

### Pydantic

Used for structured validation of AI and external-service outputs.

### Persistence layer

Stores jobs, recruiters, evidence, enrichment results, and outreach state.

---

# 3. Agent Workflow

The workflow can be represented as:

```text
START
 ↓
Load candidate
 ↓
Analyze JD
 ↓
Analyze candidate
 ↓
Generate recruiter search queries
 ↓
Search public web
 ↓
Extract recruiter candidates
 ↓
Deduplicate
 ↓
Rank
 ↓
Present recommendations
 ↓
Human selection
 ↓
Enrichment
 ↓
Evidence collection
 ↓
Claim verification
 ↓
Generate email
 ↓
Human approval
 ↓
Send
 ↓
Persist outcome
```

---

# 4. AI vs Deterministic Responsibilities

AI should be used where interpretation is required.

### AI

- Semantic understanding
- Candidate-role matching
- Recruiter relevance reasoning
- Natural-language generation

### Deterministic

- Validation
- Deduplication
- API usage tracking
- Caching
- Persistence
- Permission checks
- Sending authorization
- Error handling

This reduces unnecessary AI dependency and improves reliability.

---

# 5. External Provider Architecture

External providers should be abstracted.

Example:

```text
EnrichmentProvider
       │
       ├── HunterProvider
       │
       └── FutureProvider
```

The rest of the application should interact with the provider interface rather than directly depending on Hunter-specific implementation details.

This improves:

- Testability
- Replaceability
- Cost management
- Resilience

---

# 6. Data Model

Core entities:

### User

- user_id
- profile
- preferences

### Job

- job_id
- company
- title
- description
- requirements

### Recruiter

- recruiter_id
- name
- company
- title
- discovery_source
- relevance_score

### Evidence

- evidence_id
- recruiter_id
- source
- claim
- supporting_content

### Contact

- recruiter_id
- email
- enrichment_provider
- confidence/status

### Outreach

- outreach_id
- recruiter_id
- job_id
- generated_content
- approval_status
- sending_status
- timestamp

---

# 7. Reliability

External services can fail.

The application should therefore distinguish:

```text
Successful
Partial success
Provider unavailable
Quota exhausted
Invalid response
System failure
```

A failed enrichment request should not necessarily prevent the user from reviewing the recruiter.

---

# 8. Cost Management

The enrichment provider represents a potentially constrained resource.

The system should:

- Cache previous results.
- Avoid duplicate lookups.
- Track usage.
- Expose provider status internally.
- Gracefully degrade when quotas are exhausted.

LLM usage should similarly be monitored by:

- Requests
- Tokens
- Cost
- Model
- Workflow step

---

# 9. Security

Production deployment should include:

- Environment-based secret management
- No API keys in source control
- Secure authentication
- Access control
- Secure email credentials
- Input validation
- Logging without secrets

---

# 10. Observability

Important events should be logged:

```text
job_analysis_started
job_analysis_completed
recruiter_search_started
recruiter_search_completed
recruiter_ranked
enrichment_requested
enrichment_completed
email_generated
email_approved
email_sent
workflow_failed
```

This enables product analytics and debugging.

---

# 11. Key Architecture Tradeoff

The system intentionally does not make the LLM responsible for the entire workflow.

A fully autonomous architecture would be simpler conceptually but harder to control.

The selected architecture separates:

**Reasoning → validation → external calls → persistence → human approval**

This provides a stronger foundation for a production system.