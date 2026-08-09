import streamlit as st
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_custom_css

st.set_page_config(page_title="Candidates", page_icon="👥", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="hero-title">👥 Candidates</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">All candidates in the AI Cohort</div>', unsafe_allow_html=True)

FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(FRONTEND_DIR, "data", "candidates.json")) as f:
    all_candidates = json.load(f)["candidates"]

search = st.text_input("Search by name or role", "")

filtered = [
    c for c in all_candidates
    if search.lower() in c["member"]["name"].lower() or search.lower() in c["member"].get("jobRole", "").lower()
]

st.caption(f"{len(filtered)} of {len(all_candidates)} candidates")

for c in filtered:
    m = c["member"]
    missions = c.get("missions", [])
    completed = sum(1 for mi in missions if mi.get("passed") is True)
    failed = sum(1 for mi in missions if mi.get("passed") is False)
    skipped = sum(1 for mi in missions if mi.get("skipped"))

    st.markdown(
        f"""<div class="row-card">
            <div class="row-title">{m['name']}</div>
            <div class="row-meta">{m.get('jobRole', 'N/A')} · {m.get('yearsExperience', '?')} yrs experience</div>
            <div class="row-meta" style="margin-top:6px;">
                ✅ {completed} passed &nbsp; ⚠️ {failed} struggled &nbsp; ⏭️ {skipped} skipped
            </div>
        </div>""",
        unsafe_allow_html=True,
    )