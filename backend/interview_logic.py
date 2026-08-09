"""
Role 2 (Data & Prompt Engineering) owns this file.
This has NO server — just functions we can test on their own.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

with open("data/curriculum.json") as f:
    _curriculum_data = json.load(f)
CURRICULUM_DAYS = _curriculum_data["days"]

def pick_focus_days(candidate: dict, already_asked: set) -> list:
    missions = candidate.get("missions", [])
    scored = []
    for m in missions:
        day = m["day"]
        if day in already_asked:
            continue
        if m.get("skipped"):
            continue
        if m.get("passed") is False:
            priority = 3
        elif m.get("attempts", 1) >= 3:
            priority = 2
        else:
            priority = 1
        scored.append((priority, day, m))

    scored.sort(key=lambda x: -x[0])

    # Fallback: no usable mission history (brand new candidate)
    if not scored:
        return pick_generic_days(already_asked)

    return scored

def pick_generic_days(already_asked: set) -> list:
    """
    Fallback for a brand-new candidate with no mission history.
    Picks a spread of curriculum days (roughly one per module) so the
    interview still covers a good breadth of topics.
    """
    scored = []
    for day_info in CURRICULUM_DAYS:
        day = day_info["day"]
        if day in already_asked:
            continue
        fake_mission = {"day": day, "title": day_info["title"]}
        scored.append((1, day, fake_mission))
    return scored


def build_system_prompt(candidate: dict) -> str:
    """This instructs the AI how to behave as an interviewer."""
    member = candidate.get("member", {})
    return f"""You are an experienced technical interviewer conducting a live interview.

Candidate: {member.get('name')}, {member.get('jobRole')}, {member.get('yearsExperience')} years experience.

Your job:
- Ask ONE question at a time about topics from their learning history.
- If their answer is vague or surface-level, ask a natural follow-up before moving on.
- If their answer is strong, acknowledge briefly and move to the next topic.
- Keep a professional, conversational tone — like a real interviewer, not a quiz bot.
- Never ask about topics they skipped in their training.
- Prioritize probing topics they struggled with (failed or took many attempts).
- Keep questions concise (1-3 sentences).
- Only ask about topics explicitly provided to you in this conversation. 
- Never invent or reference technical topics, tools, or concepts that were not given to you.
"""


def generate_next_question_llm(candidate: dict, history: list, days_covered: set, mission: dict = None) -> str:
    context_note = ""
    if mission:
        context_note = f"\n\nFocus this next question on: {mission.get('title')} (Day {mission.get('day')})."

    messages = [{"role": "system", "content": build_system_prompt(candidate) + context_note}]
    for turn in history:
        role = "assistant" if turn["role"] == "assistant" else "user"
        messages.append({"role": role, "content": turn["content"]})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=200,
            timeout=15,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] generate_next_question_llm failed: {e}")
        return "Sorry, I'm having a brief technical issue. Could you repeat or continue your last point?"


def generate_feedback_llm(history: list) -> dict:
    transcript = "\n".join(
        f"{'Interviewer' if t['role']=='assistant' else 'Candidate'}: {t['content']}"
        for t in history
    )

    prompt = f"""Based on this technical interview transcript, produce feedback as STRICT JSON only
(no markdown, no explanation) with exactly these keys:
{{
  "score": <integer 0-100 reflecting overall technical performance>,
  "summary": "2-3 sentence overall assessment",
  "strengths": ["point 1", "point 2"],
  "gaps": ["point 1", "point 2"],
  "next": ["actionable recommendation 1", "actionable recommendation 2"]
}}

Score guidance: 80-100 = excellent understanding across topics, 60-79 = good with some
gaps, below 60 = significant gaps needing further study.

Transcript:
{transcript}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400,
            timeout=15,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(raw)
        parsed["score"] = max(0, min(100, int(parsed.get("score", 0))))
        return parsed
    except Exception as e:
        print(f"[ERROR] generate_feedback_llm failed: {e}")
        return {
            "score": 0,
            "summary": "We were unable to generate detailed feedback due to a technical issue.",
            "strengths": [],
            "gaps": [],
            "next": ["Please review the interview transcript manually."],
        }