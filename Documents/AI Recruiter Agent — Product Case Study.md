# AI Recruiter Agent
## Turning job applications into targeted recruiter outreach

### Overview

Applying for jobs is not only a job-discovery problem. For many candidates, the harder problem is identifying the right people to contact, determining whether those people are relevant to a specific role, finding reliable contact information, and writing outreach that is genuinely personalized.

I designed and built an AI-powered recruiter outreach agent that turns a job description and candidate profile into a targeted recruiter outreach workflow.

The product combines job-description analysis, recruiter discovery, relevance ranking, contact enrichment, evidence-based personalization, and human approval into one workflow.

---

## 1. Problem

Job seekers often approach applications as isolated submissions:

1. Find a job.
2. Read the job description.
3. Apply.
4. Hope to hear back.

This process misses an important opportunity: reaching the people involved in recruiting for the role.

Finding the right recruiter manually is time-consuming because the user must:

- Understand the role and hiring function.
- Search for relevant recruiters.
- Determine whether each recruiter actually works on the relevant function.
- Find contact information.
- Research the recruiter and company.
- Write a personalized message.
- Repeat the process for every application.

The problem is therefore not simply "write an email."

The problem is:

> **How might we reduce the time and effort required to identify and contact the most relevant recruiters for a specific job while maintaining accuracy, relevance, and user control?**

---

## 2. Target User

### Primary user

Students and early-career professionals actively applying for jobs who want to supplement applications with targeted recruiter outreach.

### User characteristics

The target user typically:

- Applies to multiple jobs.
- Has a resume and target roles.
- Has limited time for manual recruiter research.
- Wants personalized outreach rather than generic mass emails.
- Is comfortable reviewing AI-generated recommendations.
- Wants to remain in control of who receives an email.

---

## 3. Existing Workflow

A typical manual workflow looks like:

```text
Find job
   ↓
Read job description
   ↓
Identify target function
   ↓
Search company
   ↓
Search for recruiters
   ↓
Open profiles/search results
   ↓
Determine relevance
   ↓
Find email
   ↓
Research recruiter
   ↓
Write personalized message
   ↓
Review
   ↓
Send
```

The workflow contains substantial repetitive work.

The product opportunity is to automate the repetitive parts while keeping the user involved in consequential decisions.

---

## 4. Product Hypothesis

If an AI agent can understand the job requirements, discover potentially relevant recruiters, rank them using role/company/function relevance, enrich contact information, and generate evidence-backed outreach, then users should be able to conduct targeted recruiter outreach substantially faster than through a fully manual workflow.

---

## 5. Product Vision

> **Make targeted recruiter outreach as simple as reviewing a shortlist and approving a message.**

The long-term product vision is not an autonomous email bot.

It is a **human-controlled recruiting outreach copilot** that helps users make better outreach decisions while removing repetitive research work.

---

## 6. MVP

The MVP focuses on the highest-value workflow:

```text
Job Description + Resume
          ↓
   JD / Profile Analysis
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
Personalized Email Generation
          ↓
      Human Review
```

### MVP includes

- Job-description analysis
- Resume/profile analysis
- Recruiter discovery using public web search
- Recruiter relevance ranking
- User selection
- Email enrichment
- Evidence-based personalization
- AI-generated outreach
- Human approval before sending
- Usage tracking
- Persistence of product state

### MVP excludes

- Automated LinkedIn scraping
- Fully autonomous outreach
- Unreviewed bulk email sending
- Complex CRM functionality
- Large-scale enterprise recruiting workflows

---

## 7. Key Product Decisions

### Decision 1: Use public web search for recruiter discovery

Rather than building direct LinkedIn automation, the MVP uses DDG/DDGS-based public web search to discover potentially relevant recruiter information.

This reduces dependency on direct platform automation and keeps the discovery layer separated from enrichment.

### Decision 2: Keep a human in the loop

The system recommends recruiters and generates outreach, but the user decides whether to send.

This reduces the risk of:

- Incorrect recruiter targeting
- Bad personalization
- Hallucinated claims
- Unwanted outreach

### Decision 3: Separate discovery from enrichment

Discovery answers:

> "Who might be relevant?"

Enrichment answers:

> "Can we obtain reliable contact information?"

This separation allows the enrichment provider to be replaced without redesigning recruiter discovery.

### Decision 4: Require evidence for personalization

The system should not invent details about a recruiter.

Personalization claims should be traceable to evidence collected during the workflow.

---

## 8. User Experience

The intended experience is:

```text
Upload Resume
      ↓
Paste Job Description
      ↓
Analyze Match
      ↓
View Recruiter Recommendations
      ↓
Select Recruiter
      ↓
View Contact / Evidence
      ↓
Generate Outreach
      ↓
Edit / Approve
      ↓
Send
```

The product deliberately introduces a human approval step before communication is sent.

---

## 9. AI Architecture

The product uses AI for tasks where unstructured reasoning is valuable:

- Understanding job requirements
- Understanding candidate experience
- Matching candidate experience to role requirements
- Reasoning about recruiter relevance
- Generating personalized outreach

Traditional deterministic logic is retained for tasks where reliability matters more:

- Schema validation
- Data validation
- Deduplication
- Usage tracking
- Persistence
- Provider response validation

---

## 10. Success Metrics

### Primary metric

**Qualified outreach efficiency**

Time required to produce one high-quality recruiter outreach opportunity.

### Supporting metrics

- Recruiters discovered per job
- Relevant recruiter precision
- Contact enrichment success rate
- Personalization accuracy
- Email approval rate
- Average time saved
- Email response rate
- User retention
- Cost per qualified outreach

---

## 11. Current Status

The product has progressed through problem definition, MVP definition, PRD development, technical architecture, and initial implementation.

The remaining product lifecycle is:

```text
Implementation
      ↓
Systematic QA
      ↓
Internal alpha
      ↓
Real-user pilot
      ↓
Measurement
      ↓
Iteration
      ↓
Production readiness
      ↓
Launch
```

The next major objective is therefore not simply adding more features.

It is validating whether the product reliably produces useful recruiter recommendations and high-quality outreach.

---

## 12. Key Learning

The central product insight is:

> **The value is not in generating an email. The value is reducing the entire decision-making and research workflow required to produce a targeted, credible outreach opportunity.**