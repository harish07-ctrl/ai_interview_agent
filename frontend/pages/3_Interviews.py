import streamlit as st
import requests
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_custom_css

st.set_page_config(page_title="Interviews", page_icon="🎤", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="hero-title">🎤 Interviews</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">All completed interview sessions</div>', unsafe_allow_html=True)

RENDER_BASE = "https://ai-interview-agent-qglf.onrender.com"


def load_log():
    try:
        response = requests.get(f"{RENDER_BASE}/api/interview-log", timeout=15)
        return response.json()
    except Exception:
        return []


log = load_log()

if not log:
    st.info("No interviews have been conducted yet.")
else:
    st.caption(f"{len(log)} interview{'s' if len(log) != 1 else ''} completed")
    for record in reversed(log):
        st.markdown(
            f"""<div class="row-card">
                <div class="row-title">{record['candidate_name']}</div>
                <div class="row-meta">{record['timestamp'][:19].replace('T', ' at ')}</div>
                <div class="row-meta" style="margin-top:6px;">
                    {record.get('questions_asked', '?')} questions asked
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
    st.caption("For detailed strengths, gaps, and feedback, see the 💬 All Feedback page (host only).")