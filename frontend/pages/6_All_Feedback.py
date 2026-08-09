import streamlit as st
import requests
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_custom_css

st.set_page_config(page_title="Host Dashboard", page_icon="🔒", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="hero-title">🔒 Host Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI Interview Performance</div>', unsafe_allow_html=True)

RENDER_BASE = "https://ai-interview-agent-qglf.onrender.com"
FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_log():
    try:
        response = requests.get(f"{RENDER_BASE}/api/interview-log", timeout=15)
        return response.json()
    except Exception:
        return []


def clear_log():
    requests.post(f"{RENDER_BASE}/api/interview-log/clear", timeout=15)


def delete_entry(index):
    requests.post(f"{RENDER_BASE}/api/interview-log/delete", json={"index": index}, timeout=15)


def status_for_score(score):
    if score >= 80:
        return "Excellent", "#4ADE80"
    elif score >= 60:
        return "Good", "#FBBF24"
    else:
        return "Needs Help", "#F87171"


# ---- Password gate ----
if "host_unlocked" not in st.session_state:
    st.session_state.host_unlocked = False

if not st.session_state.host_unlocked:
    st.info("This page is restricted to the host.")
    entered = st.text_input("Enter host password", type="password")
    if st.button("Unlock"):
        if entered == st.secrets.get("HOST_PASSWORD", ""):
            st.session_state.host_unlocked = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# ---- Everything below only runs once unlocked ----
with open(os.path.join(FRONTEND_DIR, "data", "candidates.json")) as f:
    all_candidates = json.load(f)["candidates"]

log = load_log()

if not log:
    st.info("No interviews completed yet.")
    st.stop()

# ---- Dashboard stats ----
total_candidate_pool = len(all_candidates)
interviewed_ids = set(r.get("candidate_id", r["candidate_name"]) for r in log)
total_candidates_seen = max(total_candidate_pool, len(interviewed_ids))
interviews_completed = len(log)

scores = [r["feedback"].get("score", 0) for r in log if "feedback" in r]
avg_score = round(sum(scores) / len(scores)) if scores else 0
needing_help = sum(1 for s in scores if s < 60)

col1, col2, col3, col4 = st.columns(4)
for col, number, label in [
    (col1, total_candidates_seen, "Total Candidates"),
    (col2, interviews_completed, "Interviews Completed"),
    (col3, f"{avg_score}%", "Average Score"),
    (col4, needing_help, "Candidates Needing Help"),
]:
    with col:
        st.markdown(
            f"""<div class="stat-card" style="text-align:center;">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>""",
            unsafe_allow_html=True,
        )

st.divider()
st.markdown('<div class="section-label">📊 Candidate Performance</div>', unsafe_allow_html=True)

if st.button("Delete ALL feedback", type="primary"):
    clear_log()
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

for i in reversed(range(len(log))):
    record = log[i]
    fb = record.get("feedback", {})
    score = fb.get("score", 0)
    status, color = status_for_score(score)

    col_a, col_b, col_c, col_d = st.columns([3, 1, 1.5, 1])
    with col_a:
        st.write(f"**{record['candidate_name']}**")
    with col_b:
        st.write(f"{score}%")
    with col_c:
        st.markdown(f'<span style="color:{color}; font-weight:600;">{status}</span>', unsafe_allow_html=True)
    with col_d:
        view_clicked = st.button("View", key=f"view_{i}")

    if view_clicked:
        st.session_state[f"expanded_{i}"] = not st.session_state.get(f"expanded_{i}", False)

    if st.session_state.get(f"expanded_{i}", False):
        with st.container():
            st.write("**Summary:**", fb.get("summary"))
            st.write("**Strengths:**")
            for s in fb.get("strengths", []):
                st.write("-", s)
            st.write("**Gaps:**")
            for g in fb.get("gaps", []):
                st.write("-", g)
            st.write("**Next steps:**")
            for n in fb.get("next", []):
                st.write("-", n)
            if st.button("Delete this feedback", key=f"delete_{i}"):
                delete_entry(i)
                st.rerun()

    st.divider()