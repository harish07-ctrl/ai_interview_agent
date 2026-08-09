import streamlit as st
import requests
import os
import sys
import json
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_custom_css

st.set_page_config(page_title="Analytics", page_icon="📊", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="hero-title">📊 Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Aggregate stats across all interviews</div>', unsafe_allow_html=True)

RENDER_BASE = "https://ai-interview-agent-qglf.onrender.com"
FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_log():
    try:
        response = requests.get(f"{RENDER_BASE}/api/interview-log", timeout=15)
        return response.json()
    except Exception:
        return []


with open(os.path.join(FRONTEND_DIR, "data", "candidates.json")) as f:
    all_candidates = json.load(f)["candidates"]

log = load_log()

if not log:
    st.info("No interview data yet — analytics will appear once interviews are completed.")
else:
    total_interviews = len(log)
    unique_candidates = len(set(r["candidate_name"] for r in log))
    avg_questions = sum(r.get("questions_asked", 0) for r in log) / total_interviews
    coverage_pct = round(100 * unique_candidates / len(all_candidates), 1)

    col1, col2, col3, col4 = st.columns(4)
    for col, number, label in [
        (col1, total_interviews, "Interviews"),
        (col2, unique_candidates, "Unique Candidates"),
        (col3, round(avg_questions, 1), "Avg Questions"),
        (col4, f"{coverage_pct}%", "Cohort Coverage"),
    ]:
        with col:
            st.markdown(
                f"""<div class="stat-card" style="text-align:center;">
                    <div class="stat-number">{number}</div>
                    <div class="stat-label">{label}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-label">Most Common Gaps Identified</div>', unsafe_allow_html=True)

    all_gaps = []
    for r in log:
        all_gaps.extend(r.get("feedback", {}).get("gaps", []))

    if all_gaps:
        # crude keyword frequency: count meaningful words across all gap descriptions
        words = Counter()
        for g in all_gaps:
            for w in g.lower().split():
                w = w.strip(".,!?")
                if len(w) > 4:
                    words[w] += 1
        top_words = dict(words.most_common(8))
        if top_words:
            st.bar_chart(top_words)
    else:
        st.caption("No gap data yet.")