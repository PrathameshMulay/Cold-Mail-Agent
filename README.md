# Cold Mail Agent

AI-powered cold email agent that analyzes a job description and resume, discovers relevant recruiters, and generates a personalized outreach email.

## Features

- Job description analysis
- Resume upload via PDF
- Resume and job matching
- City-first recruiter discovery
- Target-company validation
- Company-wide fallback when local recruiters are insufficient
- Recruiter filtering and ranking
- Recruiter selection before email generation
- Email discovery using Hunter
- Evidence-backed personalized cold emails
- Automated evaluation test cases

## Workflow

```text
Job Description + Resume PDF
            ↓
      Job Analysis
            ↓
      Resume Analysis
            ↓
   Recruiter Discovery
            ↓
    Target Company Filter
            ↓
       Max 10 Recruiters
            ↓
     Recruiter Ranking
            ↓
     User Selects Recruiter
            ↓
       Hunter Email Search
            ↓
      Evidence Matching
            ↓
     Personalized Email