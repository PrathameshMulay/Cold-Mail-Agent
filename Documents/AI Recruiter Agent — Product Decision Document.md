# AI Recruiter Agent
## Product Decision Document

**Product:** AI Recruiter Agent  
**Product Type:** AI-powered career / recruiter outreach copilot  
**Stage:** MVP development  
**Document Purpose:** Record the product decisions, rationale, tradeoffs, and implications behind the product.

---

# 1. Product Context

## 1.1 Product Vision

The AI Recruiter Agent is designed to help job seekers turn a job opportunity into targeted recruiter outreach.

The product should reduce the repetitive research involved in:

- Understanding a job opportunity
- Finding relevant recruiters
- Determining recruiter relevance
- Finding contact information
- Researching supporting information
- Creating personalized outreach

The product is intended to function as a **recruiter outreach copilot**, rather than simply an AI email generator.

---

# 2. Core Product Problem

## Decision

The product will focus on the broader recruiter-outreach workflow rather than only email generation.

### Problem

A job seeker may find a job they want to apply for but still need to manually:

1. Understand the role.
2. Determine what type of recruiter is relevant.
3. Search for recruiters.
4. Determine which recruiter is actually relevant.
5. Find contact information.
6. Research the recruiter/company.
7. Write personalized outreach.
8. Review the message.
9. Send it.

This creates a repetitive workflow with significant manual effort.

### Product opportunity

Automate the research-heavy portions of the workflow while leaving important professional decisions under user control.

---

# 3. Target User

## Decision

The initial product is targeted at individual job seekers rather than companies.

### Primary user

Students and early-career professionals actively applying for jobs.

### Why this segment

The workflow is:

- Repetitive
- Research-heavy
- Time-consuming
- Relevant across multiple job applications
- Suitable for AI-assisted automation

### Explicit product positioning

This is a **B2C / individual-user product**, not an enterprise recruiting platform.

The product should therefore optimize for:

- Simplicity
- Fast time-to-value
- Low setup friction
- Individual workflow
- User control
- Affordable API/AI usage

---

# 4. Product Vision

## Decision

The long-term product vision is:

> **Make targeted recruiter outreach as simple as reviewing a shortlist and approving a message.**

The product should eventually move toward a workflow where the user provides a job opportunity and receives:

- Relevant recruiter recommendations
- Evidence explaining those recommendations
- Contact information where available
- Personalized outreach
- A clear approval workflow

---

# 5. Core Product Philosophy

## Decision

The product should automate **research and preparation**, not blindly automate professional communication.

The fundamental product principle is:

> **Automate research → explain recommendations → let the user decide → assist with communication.**

This creates a human-in-the-loop product rather than a fully autonomous outreach bot.

---

# 6. MVP Scope

## Decision

The MVP will focus on the following workflow:

```text
Job Description
       +
Candidate Profile
       ↓
Job Analysis
       ↓
Recruiter Discovery
       ↓
Recruiter Ranking
       ↓
User Selection
       ↓
Contact Enrichment
       ↓
Evidence Collection
       ↓
Personalized Outreach
       ↓
Human Review
       ↓
Send
```

---

# 7. MVP Feature Decisions

## 7.1 Job Description Analysis

### Decision

The system will analyze the job description to understand the opportunity.

It should identify information such as:

- Role
- Company
- Functional area
- Required skills
- Preferred skills
- Experience requirements
- Seniority
- Relevant keywords

### Important scope decision

The job-analysis component is **not intended to compare the job description against the user's resume or produce a candidate-role fit score**.

Its purpose is to understand the job so that downstream recruiter discovery, ranking, and outreach can be informed by the opportunity.

---

# 8. Candidate Information

## Decision

The user's resume/profile provides candidate context for the outreach workflow.

The system may extract:

- Skills
- Experience
- Education
- Projects
- Previous roles
- Relevant background

This information is primarily used to provide context for outreach generation and recruiter targeting.

---

# 9. Recruiter Discovery

## Decision

Recruiter discovery will use public web search rather than direct LinkedIn automation.

### Selected approach

DDG/DDGS-based web search.

### Why

The product needs a discovery mechanism capable of identifying potentially relevant recruiters without making direct LinkedIn scraping/automation the core dependency.

### Discovery workflow

```text
Job / Company / Function
        ↓
Search query generation
        ↓
Public web search
        ↓
Potential recruiter results
        ↓
Extraction
        ↓
Deduplication
        ↓
Relevance evaluation
```

### Tradeoff

Public search may provide less structured information than a dedicated professional-network data source.

However, it provides a simpler MVP architecture and avoids making direct LinkedIn automation a core product dependency.

---

# 10. Recruiter Discovery vs Recruiter Ranking

## Decision

These are separate product problems.

### Discovery asks:

> "Who might be relevant?"

### Ranking asks:

> "Which discovered recruiters are most relevant?"

This distinction is important because finding someone with the title "Recruiter" is not sufficient.

A recruiter may be:

- In the wrong function
- In the wrong business unit
- Recruiting for a different role
- In a different geography
- No longer associated with the relevant hiring area

Therefore, discovery volume should not be treated as product success.

---

# 11. Recruiter Ranking

## Decision

Recruiters should be ranked using multiple relevance signals rather than title alone.

Potential signals include:

- Company match
- Functional-area match
- Role match
- Recruiting responsibility
- Seniority
- Geography when relevant
- Evidence strength

### Product principle

The system should explain **why** a recruiter was ranked highly.

Example:

```text
Recruiter: Jane Doe
Company: Example Corp
Function: Talent Acquisition

Relevance: High

Why:
• Associated with the target company
• Evidence indicates recruiting responsibility
• Relevant functional alignment
```

The user should not have to blindly trust a numerical score.

---

# 12. Evidence as a Product Feature

## Decision

Evidence should be treated as a first-class product capability.

The system should distinguish between:

### Evidence

Information discovered from external sources.

### Inference

The system's conclusion based on that information.

### Generated content

Text produced by the AI using the available information.

Example:

```text
Evidence
↓
"Jane Doe recruits for Data & Analytics roles."

Inference
↓
"Jane Doe is likely relevant to this analytics position."

Generated content
↓
"Your work recruiting analytics talent caught my attention..."
```

This separation improves transparency and reduces unsupported AI-generated claims.

---

# 13. Personalization

## Decision

Outreach should be personalized using information that can be supported by available evidence.

The system should avoid inventing:

- Recruiter responsibilities
- Company facts
- Recruiter interests
- Shared experiences
- Hiring relationships
- Other unsupported details

### Product principle

**Personalization quality is more important than personalization quantity.**

A short, accurate message is preferable to an impressive-sounding message containing fabricated information.

---

# 14. Contact Enrichment

## Decision

Recruiter discovery and contact enrichment are separate components.

### Discovery

Finds potentially relevant recruiters.

### Enrichment

Attempts to obtain contact information for a selected recruiter.

### Selected enrichment provider

Hunter.

### Why this architecture

The system should not tightly couple recruiter discovery to a single enrichment provider.

The architecture should conceptually look like:

```text
                 Enrichment Interface
                         │
                         ▼
                    Hunter
                         │
              Future provider(s)
```

This provides flexibility if:

- Pricing changes
- Quotas change
- Availability changes
- Another provider produces better results

---

# 15. Hunter Usage / Quota Management

## Decision

Enrichment usage must be actively controlled.

The product should not call Hunter unnecessarily.

### Required controls

- Track enrichment requests
- Prevent duplicate lookups
- Cache results when appropriate
- Handle quota exhaustion
- Handle provider failures
- Avoid repeated requests for the same recruiter

### Product reason

External API limits are not merely an engineering problem.

They directly affect:

- Product cost
- User experience
- Scalability
- Reliability

Therefore, usage management is part of the product design.

---

# 16. Human-in-the-Loop Decision

## Decision

The system will not automatically send recruiter outreach without explicit user approval.

The workflow is:

```text
AI recommendation
       ↓
User reviews recruiter
       ↓
AI generates message
       ↓
User reviews message
       ↓
User approves
       ↓
Send
```

### Why

The email represents the user's professional identity.

An incorrect recruiter recommendation or hallucinated claim can damage the user's credibility.

The user therefore remains the final decision-maker.

---

# 17. Email Generation

## Decision

The AI should generate the outreach message after recruiter selection and evidence collection.

The message should incorporate:

- Target job
- Company
- Candidate context
- Recruiter context
- Verified evidence
- Appropriate personalization

The user should be able to:

- Edit
- Regenerate
- Remove content
- Change tone
- Reject
- Approve

---

# 18. AI vs Deterministic Logic

## Decision

The LLM should not control the entire application.

AI is best suited to:

- Understanding unstructured job descriptions
- Extracting semantic information
- Reasoning about recruiter relevance
- Generating personalized language

Deterministic application logic should handle:

- Validation
- Deduplication
- Persistence
- API usage
- Caching
- Permission checks
- Approval state
- Sending authorization
- Error handling

### Rationale

Using an LLM for every operation increases:

- Cost
- Latency
- Unpredictability
- Failure modes

The product therefore uses AI where reasoning creates value and traditional software where deterministic behavior is preferable.

---

# 19. Structured AI Outputs

## Decision

AI outputs should be structured and validated rather than treated as arbitrary text.

A schema-validation layer should be used for important AI outputs.

The purpose is to prevent downstream components from assuming that the LLM always returns valid information.

Conceptually:

```text
LLM
 ↓
Structured output
 ↓
Schema validation
 ↓
Application logic
```

If validation fails, the application should handle the failure rather than blindly passing the output downstream.

---

# 20. Multi-Agent / Agentic Architecture

## Decision

The product should be treated as an agentic workflow where specialized tasks can be separated rather than creating one giant AI prompt.

Conceptually:

```text
                Orchestrator
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   Job Analysis   Recruiter    Candidate
                  Discovery    Analysis
                       ↓
                  Recruiter
                    Ranking
                       ↓
                  Enrichment
                       ↓
                   Evidence
                       ↓
                   Outreach
```

The orchestration layer determines which capability is required at each stage.

The goal is not to maximize the number of agents.

The goal is to create clear responsibility boundaries.

---

# 21. Persistence

## Decision

The product should persist important workflow information rather than treating each execution as a disposable AI conversation.

Important persistent objects include:

### Job

- Job ID
- Company
- Role
- Job description
- Extracted requirements

### Recruiter

- Recruiter ID
- Name
- Company
- Title
- Discovery source
- Relevance information

### Evidence

- Evidence ID
- Recruiter
- Source
- Claim
- Supporting information

### Contact

- Recruiter
- Email/contact information
- Provider
- Status

### Outreach

- Recruiter
- Job
- Generated message
- Approval state
- Sending state
- Timestamp

---

# 22. Why Persistence Matters

Persistence allows the product to eventually prevent users from repeating work.

For example:

```text
User previously researched:
Jane Doe
Example Corp
Data Recruiting

New job at Example Corp
        ↓
System recognizes Jane Doe
        ↓
Existing information reused
```

This creates increasing value as the user uses the product repeatedly.

---

# 23. Error Handling

## Decision

External failures should not automatically terminate the entire workflow.

Potential failure states include:

```text
Search failure
Enrichment failure
Quota exhausted
Invalid AI output
Missing evidence
Email generation failure
Email sending failure
```

The UI should explain the failure and preserve whatever useful work has already been completed.

---

# 24. Cost Control

## Decision

AI and external API usage should be treated as product resources.

The system should track:

- LLM calls
- Model usage
- Token usage where available
- Search requests
- Enrichment requests
- Failed requests
- Cached requests

### Principle

Do not spend an API call when existing information can answer the question.

This is particularly important for the enrichment layer.

---

# 25. User Experience

## Decision

The core UX should be simple enough that the user does not need to understand the underlying agent architecture.

The user sees:

```text
1. Provide job
2. Provide profile
3. Review recruiter recommendations
4. Select recruiter
5. Review contact/evidence
6. Review outreach
7. Approve
8. Send
```

The complexity belongs behind the interface.

---

# 26. Transparency

## Decision

The UI should expose enough information for users to understand important AI decisions.

For recruiter recommendations, the user should be able to answer:

> "Why did the system recommend this person?"

For outreach, the user should be able to answer:

> "Where did this personalization come from?"

This is a core trust mechanism.

---

# 27. Product Scope Decisions

## Included in MVP

- Job analysis
- Candidate context
- Recruiter discovery
- Recruiter ranking
- Contact enrichment
- Evidence
- Personalized outreach
- Human review
- Sending
- Persistence
- Usage tracking

## Explicitly excluded from MVP

- Direct LinkedIn scraping
- Fully autonomous outreach
- Unreviewed bulk sending
- Full recruiting CRM
- Enterprise recruiting workflows
- Large-scale recruiting automation

---

# 28. Key Product Tradeoffs

## Tradeoff 1 — Automation vs control

### Option

Fully autonomous outreach.

### Decision

Human approval.

### Reason

Professional communication carries reputational risk.

### Cost

The product requires one additional human step.

### Benefit

Higher user control and trust.

---

## Tradeoff 2 — Search quality vs implementation simplicity

### Option

Build around direct professional-network automation.

### Decision

Public web search using DDG/DDGS.

### Reason

Simpler MVP and reduced dependency on direct LinkedIn automation.

### Cost

Potentially lower or less structured discovery quality.

### Mitigation

Improve query generation, filtering, ranking, and evaluation.

---

## Tradeoff 3 — One large AI agent vs specialized workflow

### Option

One general-purpose agent handles everything.

### Decision

Separate responsibilities into specialized workflow components.

### Reason

Clearer responsibilities, easier debugging, better control, and more targeted evaluation.

### Cost

More orchestration complexity.

---

## Tradeoff 4 — AI everywhere vs deterministic software

### Option

Use the LLM for every decision.

### Decision

Use AI only where semantic reasoning is valuable.

### Reason

Lower cost, better reliability, and easier testing.

---

## Tradeoff 5 — Maximum personalization vs evidence-backed personalization

### Option

Generate highly creative personalization.

### Decision

Prioritize evidence-backed personalization.

### Reason

Accuracy and trust are more valuable than superficial personalization.

---

## Tradeoff 6 — Maximum API usage vs controlled API usage

### Option

Call enrichment APIs whenever additional information might help.

### Decision

Use caching, deduplication, and usage controls.

### Reason

API quotas and costs directly affect product economics.

---

# 29. Success Metrics

The product should not be judged primarily by whether the AI produces an email.

The key question is:

> **Does the product help a user produce a qualified recruiter outreach opportunity faster and with sufficient confidence?**

## Primary metric

### Qualified outreach efficiency

Time and effort required to produce a qualified recruiter outreach opportunity.

---

## Supporting metrics

### Discovery

- Recruiters discovered
- Relevant recruiter precision
- Top-3 relevance

### Enrichment

- Enrichment success rate
- Valid contact rate
- Cost per successful enrichment

### AI quality

- Personalization accuracy
- Unsupported claim rate
- Email approval rate
- Editing rate
- Regeneration rate

### User value

- Time saved
- Workflow completion rate
- Repeat usage
- User satisfaction

### Outcome

- Emails sent
- Recruiter response rate
- Positive response rate

---

# 30. Evaluation Strategy

## Decision

The product must be evaluated on both **AI quality** and **product value**.

### Experiment 1 — Recruiter discovery

Measure whether discovered recruiters are actually relevant.

### Experiment 2 — Recruiter ranking

Measure whether the most relevant recruiters appear near the top.

### Experiment 3 — Personalization

Evaluate generated emails for:

- Accuracy
- Evidence
- Relevance
- Personalization
- Professionalism
- Clarity

### Experiment 4 — Time savings

Compare manual recruiter outreach preparation against the agent-assisted workflow.

### Experiment 5 — Enrichment

Measure:

- Success rate
- Cost
- Duplicate requests
- Provider failures

### Experiment 6 — End-to-end workflow

Measure the percentage of users/workflows successfully moving from:

```text
Job
 ↓
Recruiter
 ↓
Contact
 ↓
Evidence
 ↓
Email
 ↓
Approval
 ↓
Send
```

---

# 31. Validation Philosophy

## Decision

A functioning application is not sufficient evidence of product-market value.

The product needs to demonstrate:

1. It finds relevant recruiters.
2. It ranks useful recruiters highly.
3. It produces accurate personalization.
4. It saves meaningful user time.
5. Users trust the recommendations.
6. Users actually use the resulting outreach.

---

# 32. Current Product Stage

The product has progressed through:

- Problem definition
- Product vision
- MVP definition
- Product requirements
- UX/product-flow definition
- Technical discovery
- Architecture
- Initial implementation

The product has **not yet completed**:

- Formal external user validation
- Systematic QA
- Internal alpha
- Customer beta
- Production-readiness review
- Public launch
- Post-launch measurement

These should therefore remain future milestones rather than being represented as completed achievements.

---

# 33. Next Product Decisions

The next major decisions should be driven by evidence.

### Decision area 1

How accurately does the system identify relevant recruiters?

### Decision area 2

Which ranking signals actually improve recruiter relevance?

### Decision area 3

How much editing do users perform on generated emails?

### Decision area 4

How often does the system produce unsupported claims?

### Decision area 5

How much time does the product actually save?

### Decision area 6

Does recruiter outreach improve meaningful job-search outcomes?

---

# 34. Product Evolution

The intended evolution is:

```text
MVP
AI Recruiter Discovery
        ↓
AI Recruiter Outreach Copilot
        ↓
Recruiter Outreach Intelligence
        ↓
Broader Career Outreach Platform
```

However, future features should be driven by validated user needs rather than simply increasing the number of AI capabilities.

---

# 35. Decision-Making Framework

For future product decisions, use:

```text
Problem
   ↓
Evidence
   ↓
Options
   ↓
Tradeoffs
   ↓
Decision
   ↓
Implementation
   ↓
Measurement
   ↓
Learning
```

Every significant product decision should answer:

1. What problem are we solving?
2. What alternatives did we consider?
3. Why did we choose this approach?
4. What are we giving up?
5. What risk does this introduce?
6. How will we know whether the decision was correct?

---

# 36. Current Product Thesis

The current thesis is:

> **Job seekers do not primarily need another AI email writer. They need an intelligent system that reduces the research and decision-making effort required to identify the right recruiter and produce credible, personalized outreach.**

The product therefore differentiates itself through the combination of:

**Discovery + Ranking + Enrichment + Evidence + Personalization + Human Control**

rather than through email generation alone.

---

# 37. Summary of Major Decisions

| Area | Decision |
|---|---|
| Target market | Individual job seekers |
| Product type | AI recruiter outreach copilot |
| Core problem | Research-heavy recruiter outreach |
| Job analysis | Understand role/opportunity |
| Candidate analysis | Provide candidate context |
| Recruiter discovery | Public web search |
| Search technology | DDG/DDGS |
| Recruiter ranking | Multi-signal relevance |
| Contact enrichment | Hunter |
| Enrichment architecture | Provider abstraction |
| Personalization | Evidence-backed |
| AI output | Structured + validated |
| AI architecture | Specialized workflow components |
| Human involvement | Required before sending |
| Persistence | Required for workflow state |
| API management | Track, cache, control usage |
| MVP focus | End-to-end recruiter outreach |
| Direct LinkedIn automation | Excluded from MVP |
| Autonomous sending | Excluded |
| Main success metric | Qualified outreach efficiency |
| Primary validation | Recruiter relevance + time saved |
| Current stage | MVP implementation |
| Next stage | QA → alpha → pilot → validation |