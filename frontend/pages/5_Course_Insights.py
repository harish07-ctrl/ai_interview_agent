import streamlit as st
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_custom_css

st.set_page_config(page_title="Course Insights", page_icon="📚", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="hero-title">📚 Course Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Which curriculum topics the cohort struggles with most</div>', unsafe_allow_html=True)

FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(FRONTEND_DIR, "data", "candidates.json")) as f:
    all_candidates = json.load(f)["candidates"]
with open(os.path.join(FRONTEND_DIR, "data", "curriculum.json")) as f:
    curriculum = json.load(f)

day_titles = {d["day"]: d["title"] for d in curriculum["days"]}

# Aggregate pass/fail counts per day across every candidate
struggle_counts = {}
attempt_counts = {}
for c in all_candidates:
    for mi in c.get("missions", []):
        if mi.get("skipped"):
            continue
        day = mi["day"]
        attempt_counts[day] = attempt_counts.get(day, 0) + 1
        if mi.get("passed") is False:
            struggle_counts[day] = struggle_counts.get(day, 0) + 1

# Compute a struggle rate per day, only for days with real attempts
rates = {}
for day, attempts in attempt_counts.items():
    fails = struggle_counts.get(day, 0)
    if attempts >= 2:  # ignore days with too little data to be meaningful
        rates[f"Day {day}: {day_titles.get(day, 'Unknown')}"] = round(100 * fails / attempts, 1)

st.markdown('<div class="section-label">Struggle Rate by Topic (% of attempts that failed)</div>', unsafe_allow_html=True)

if rates:
    sorted_rates = dict(sorted(rates.items(), key=lambda x: -x[1])[:10])
    st.bar_chart(sorted_rates)

    hardest = max(rates, key=rates.get)
    st.caption(f"Hardest topic overall: **{hardest}** ({rates[hardest]}% struggle rate)")
else:
    st.info("Not enough mission data to compute insights yet.")

st.divider()
st.markdown('<div class="section-label">All Curriculum Days</div>', unsafe_allow_html=True)
for module in curriculum["modules"]:
    with st.expander(f"Module {module['n']}: {module['title']}"):
        start, end = module["days"]
        for day_info in curriculum["days"]:
            if start <= day_info["day"] <= end:
                st.write(f"**Day {day_info['day']}:** {day_info['title']}")