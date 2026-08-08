"""
AI Interview Agent — Backend
Role 1 owns this file.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
from groq import Groq
from interview_logic import pick_focus_days, generate_next_question_llm, generate_feedback_llm
import json 
from datetime import datetime

load_dotenv()  # reads your .env file so GROQ_API_KEY becomes available

app = FastAPI()

# Allow the frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ---- In-memory session store ----
sessions: Dict[str, Dict[str, Any]] = {}

MIN_QUESTIONS = 8
MIN_DAYS = 4


class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


@app.post("/api/interview")
def interview(req: InterviewRequest):
    session_id = req.sessionId

    if req.candidate is not None and session_id not in sessions:
        sessions[session_id] = {
            "candidate": req.candidate,
            "history": [],
            "questions_asked": 0,
            "days_covered": set(),
        }
        first_question = generate_opening_question(req.candidate)
        sessions[session_id]["history"].append({"role": "assistant", "content": first_question})
        sessions[session_id]["questions_asked"] += 1
        return {"reply": first_question, "done": False, "progress": {"asked": 1, "min": MIN_QUESTIONS}}

    session = sessions.get(session_id)
    if session is None:
        return {"reply": "Session not found. Please start a new interview.", "done": True}

    session["history"].append({"role": "user", "content": req.message})

    if should_end(session):
        feedback = generate_feedback(session)
        save_completed_interview(session, feedback)
        return {
            "reply": "Interview completed. Thank you for your time.",
            "done": True,
            "feedback": feedback,
        }

    next_question = generate_next_question(session)
    session["history"].append({"role": "assistant", "content": next_question})
    session["questions_asked"] += 1
    return {"reply": next_question, "done": False, "progress": {"asked": session["questions_asked"], "min": MIN_QUESTIONS}}


def should_end(session: Dict[str, Any]) -> bool:
    hit_minimums = session["questions_asked"] >= MIN_QUESTIONS and len(session["days_covered"]) >= MIN_DAYS
    ran_out_of_topics = session.get("out_of_topics", False)
    return hit_minimums or (session["questions_asked"] >= MIN_DAYS and ran_out_of_topics)


# ---- PLACEHOLDER FUNCTIONS (Role 2 replaces these later) ----

def generate_opening_question(candidate: Dict[str, Any]) -> str:
    focus_list = pick_focus_days(candidate, already_asked=set())
    if not focus_list:
        return "Welcome! Let's start with a general question: what part of the program did you find most challenging?"
    _, day, mission = focus_list[0]
    question = generate_next_question_llm(candidate, history=[], days_covered=set(), mission=mission)
    return question


def generate_next_question(session: Dict[str, Any]) -> str:
    candidate = session["candidate"]
    history = session["history"]
    days_covered = session["days_covered"]

    focus_list = pick_focus_days(candidate, already_asked=days_covered)
    mission = None
    if focus_list:
        _, day, mission = focus_list[0]
        days_covered.add(day)
    else:
        session["out_of_topics"] = True

    return generate_next_question_llm(candidate, history, days_covered, mission=mission)



def generate_feedback(session: Dict[str, Any]) -> Dict[str, Any]:
    return generate_feedback_llm(session["history"])

def save_completed_interview(session: Dict[str, Any], feedback: Dict[str, Any]):
    """Appends this completed interview to a simple JSON log file."""
    record = {
        "candidate_name": session["candidate"].get("member", {}).get("name", "Unknown"),
        "candidate_id": session["candidate"].get("member", {}).get("id", "Unknown"),
        "timestamp": datetime.now().isoformat(),
        "questions_asked": session["questions_asked"],
        "transcript": session["history"],
        "feedback": feedback,
    }

    log_file = "interview_log.json"
    try:
        with open(log_file, "r") as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = []

    log.append(record)

    with open(log_file, "w") as f:
        json.dump(log, f, indent=2)

@app.get("/api/interview-log")
def get_interview_log():
    try:
        with open("interview_log.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@app.post("/api/interview-log/clear")
def clear_interview_log():
    with open("interview_log.json", "w") as f:
        json.dump([], f)
    return {"status": "cleared"}


@app.post("/api/interview-log/delete")
def delete_interview_log_entry(payload: dict):
    index = payload.get("index")
    try:
        with open("interview_log.json", "r") as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = []
    if index is not None and 0 <= index < len(log):
        log.pop(index)
    with open("interview_log.json", "w") as f:
        json.dump(log, f, indent=2)
    return {"status": "deleted"}