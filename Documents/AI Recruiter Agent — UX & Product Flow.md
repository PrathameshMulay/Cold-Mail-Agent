# AI Recruiter Agent

## UX & Product Flow

### 1. Design Principle

The product should minimize the amount of research the user performs without removing the user's control over professional communication.

The experience therefore follows:

> **Automate research → explain recommendations → let the user decide → assist with communication.**

---

# 2. Primary User Flow

START\
↓\
Upload / provide resume\
↓\
Paste job description\
↓\
Analyze opportunity\
↓\
Discover recruiters\
↓\
Rank recruiters\
↓\
Display evidence\
↓\
User selects recruiter\
↓\
Enrich contact information\
↓\
Generate outreach\
↓\
Display supporting evidence\
↓\
User edits / approves\
↓\
Send\
↓\
Track outreach

---

# 3. Screen 1 — Job Input

### Purpose

Allow the user to define the opportunity they want to pursue.

### Inputs

- Job description
- Company
- Role
- Resume/profile

### Primary action

**Analyze opportunity**

### Error states

- Missing job description
- Invalid input
- Processing failure

---

# 4. Screen 2 — Opportunity Analysis

Display:

### Role

Target position.

### Company

Hiring organization.

### Key requirements

- Technical skills
- Business skills
- Experience
- Education
- Other qualifications

The system uses the job description to understand the role and identify the types of recruiters who may be relevant.

It does not compare the job description with the user's resume or evaluate candidate-role alignment.

The purpose is to provide context for recruiter discovery, ranking, and outreach.

---

# 5. Screen 3 — Recruiter Recommendations

Each recruiter card should show:

- Recruiter name
- Current title
- Company
- Relevance score
- Why they were selected
- Supporting evidence
- Contact availability

Example:

```text
Recruiter Name
Talent Acquisition — Company

Relevance: High

Why:
• Recruits for target function
• Associated with target company
• Evidence indicates relevant hiring responsibility

Contact:
Email available

[View Evidence]    [Select]
```

---

# 6. Screen 4 — Evidence

The user should be able to inspect why the system considers a recruiter relevant.

The interface should distinguish:

### Evidence

Information discovered from sources.

### Inference

What the system concluded from that evidence.

### Generated content

What the AI produced using that information.

This distinction improves trust.

---

# 7. Screen 5 — Outreach Generator

The system generates:

### Subject

Role-specific subject line.

### Email

Personalized message.

### Personalization sources

Show which evidence was used.

---

# 8. Screen 6 — Human Review

The user can:

- Edit
- Regenerate
- Remove unsupported claims
- Change tone
- Approve
- Reject

The send action should require explicit user approval.

---

# 9. Screen 7 — Outreach Status

The user should eventually be able to see:

- Draft
- Approved
- Sent
- Delivered
- Replied
- Follow-up needed

This becomes the foundation for future analytics.

---

# 10. UX Principles

### Transparency

Users should understand why recommendations were made.

### Control

The system should never send consequential communication without approval.

### Evidence

AI-generated claims should be traceable.

### Progressive disclosure

Show the important recommendation first; allow users to inspect details when needed.

### Error recovery

When an external provider fails, explain what happened and allow the user to continue where possible.

---

# 11. Future UX Improvements

Potential future enhancements include:

- Saved candidate profiles
- Saved target companies
- Recruiter history
- Outreach analytics
- Follow-up recommendations
- Multiple job workflows
- Application tracking

These should be prioritized only after MVP usage demonstrates demand.
