# AI Usage Log — AI Interview Agent

This document records how AI tools were used throughout building this project,
in line with the hackathon's authenticity requirements.

## Tools used
- **Claude** (Anthropic) — architecture planning, code generation, debugging, UI/UX design
- **Groq API (Llama 3.3 70B)** — powers the live interview agent itself (question generation, follow-ups, feedback, and scoring)

## Development process

### 1. Architecture & planning
Asked Claude to explain the hackathon problem statement and technical spec, then design
a beginner-friendly architecture: FastAPI backend + Streamlit frontend, split across a
3-person team (backend/agent logic, prompt/data engineering, frontend).

### 2. Backend — question selection logic
Core prompt used to build the personalization logic:
> "Given a candidate's mission history (day, title, passed/failed, attempts), write a
> function that prioritizes which curriculum days to ask about next — prioritizing
> failed missions, then high-attempt passes, then easy passes. Skip skipped missions."

### 3. System prompt for the interviewer persona
> "Write a system prompt for an LLM acting as a technical interviewer. It should ask
> one question at a time, follow up naturally on vague answers, stay grounded strictly
> in provided curriculum topics, and never invent unrelated technical concepts."

This was iterated on after discovering the model would hallucinate off-curriculum
topics (e.g. "graph neural networks") once real candidate topics ran out — the prompt
was tightened to explicitly forbid inventing topics, and a fallback was added so the
interview ends gracefully instead of improvising.

### 4. Feedback generation & scoring
> "Given a full interview transcript, generate structured JSON feedback with an overall
> score (0-100), summary, strengths, gaps, and next steps — grounded only in what was
> actually discussed."

### 5. Frontend UI/UX
Iteratively asked Claude to design a dark, modern interface: a landing page, candidate
selector with mission history, progress tracking, a dedicated animated results screen,
a galaxy-themed background, and a multi-page host dashboard (Candidates, Interviews,
Analytics, Course Insights, and a password-protected All Feedback view) — including
debugging several CSS issues (z-index stacking conflicts with Streamlit's internal
layout, background layering).

### 6. Debugging & deployment
Used Claude throughout to debug environment issues (PATH errors with pip/uvicorn/
streamlit on Windows), fix a session-state bug causing a blank screen for new
candidates, resolve file-path issues when deploying the frontend (Streamlit Community
Cloud) and backend (Render) as separate services, and add retry/error handling for
Render's free-tier cold-start behavior.

## Summary
Every core piece of application logic — the personalization algorithm, the interview
system prompt, the feedback/scoring prompt, and the UI — was designed through
iterative conversation with Claude, then implemented, tested, and debugged as a team
across the full build.