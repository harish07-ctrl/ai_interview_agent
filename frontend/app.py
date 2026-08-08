"""
AI Interview Agent — Frontend
Role 3 owns this file.
"""

import streamlit as st
import requests
import uuid
import json
import os 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BACKEND_URL = "https://ai-interview-agent-qglf.onrender.com/api/interview"

st.set_page_config(page_title="AI Interview Agent", page_icon="🎤", layout="centered")

CUSTOM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 760px;
    }

    .stApp {
        background-color: #05050C;
        background-image:
            radial-gradient(1.5px 1.5px at 20px 30px, #ffffff, transparent),
            radial-gradient(1px 1px at 90px 80px, #ffffff, transparent),
            radial-gradient(1.5px 1.5px at 160px 40px, #C4B5FD, transparent),
            radial-gradient(1px 1px at 220px 120px, #ffffff, transparent),
            radial-gradient(1.5px 1.5px at 280px 60px, #93C5FD, transparent),
            radial-gradient(1px 1px at 340px 150px, #ffffff, transparent),
            radial-gradient(1.5px 1.5px at 50px 170px, #ffffff, transparent),
            radial-gradient(1px 1px at 380px 20px, #ffffff, transparent),
            radial-gradient(ellipse at 20% 15%, rgba(139, 92, 246, 0.25), transparent 45%),
            radial-gradient(ellipse at 80% 10%, rgba(59, 130, 246, 0.20), transparent 45%),
            radial-gradient(ellipse at 60% 80%, rgba(236, 72, 153, 0.16), transparent 50%),
            radial-gradient(ellipse at 10% 90%, rgba(99, 102, 241, 0.18), transparent 45%);
        background-repeat: repeat, repeat, repeat, repeat, repeat, repeat, repeat, repeat, no-repeat, no-repeat, no-repeat, no-repeat;
        background-size: 420px 220px, 420px 220px, 420px 220px, 420px 220px, 420px 220px, 420px 220px, 420px 220px, 420px 220px, auto, auto, auto, auto;
        background-attachment: fixed;
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: #2D2F3D;
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #3D3F52; }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #818CF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .hero-subtitle {
        color: #8B8D98;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .sidebar-section-label {
        text-transform: uppercase;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #6B6D7A;
        margin: 20px 0 10px 0;
    }
    .profile-card {
        background: linear-gradient(180deg, #1A1D29, #171A24);
        border: 1px solid #262838;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .profile-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F5F5F7;
        letter-spacing: -0.01em;
    }
    .profile-meta {
        color: #8B8D98;
        font-size: 0.85rem;
        margin-top: 2px;
    }
    .mission-badge {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 6px;
        font-size: 0.8rem;
        font-weight: 500;
        transition: transform 0.15s ease;
    }
    .mission-badge:hover { transform: translateX(2px); }
    .mission-struggled {
        background: rgba(248, 113, 113, 0.08);
        color: #F87171;
        border: 1px solid rgba(248, 113, 113, 0.18);
    }
    .mission-strong {
        background: rgba(74, 222, 128, 0.08);
        color: #4ADE80;
        border: 1px solid rgba(74, 222, 128, 0.18);
    }
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 6px 10px;
        margin-bottom: 10px;
        animation: fadeSlideIn 0.3s ease;
    }
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .results-screen {
        animation: fadeInUp 0.5s ease;
    }
    .results-title {
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    .results-subtitle {
        color: #8B8D98;
        font-size: 0.9rem;
        margin-bottom: 1.8rem;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        letter-spacing: -0.01em;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        border: none;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.3);
    }
    .stProgress > div > div > div {
        border-radius: 8px;
        background: linear-gradient(90deg, #6366F1, #A855F7);
    }
    .feedback-card {
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 16px;
        border: 1px solid;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .feedback-summary {
        background: rgba(99, 102, 241, 0.10);
        border-color: rgba(99, 102, 241, 0.22);
    }
    .feedback-strengths {
        background: rgba(34, 197, 94, 0.10);
        border-color: rgba(34, 197, 94, 0.22);
    }
    .feedback-gaps {
        background: rgba(245, 158, 11, 0.10);
        border-color: rgba(245, 158, 11, 0.22);
    }
    .feedback-next {
        background: rgba(59, 130, 246, 0.10);
        border-color: rgba(59, 130, 246, 0.22);
    }
    .feedback-card-title {
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: -0.01em;
        margin-bottom: 10px;
        opacity: 0.95;
    }
    .feedback-card ul {
        margin: 0;
        padding-left: 20px;
    }
    .feedback-card li {
        margin-bottom: 4px;
        line-height: 1.5;
    }
    hr {
        border-color: #22242F !important;
        margin: 1.5rem 0 !important;
    }

    .landing-wrap {
        text-align: center;
        padding-top: 3rem;
        animation: fadeInUp 0.6s ease;
    }
    .landing-hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(90deg, #818CF8, #C084FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .landing-subtitle {
        color: #A1A1AA;
        font-size: 1.1rem;
        max-width: 480px;
        margin: 0 auto 2.5rem auto;
        line-height: 1.6;
    }
    .feature-card {
        background: linear-gradient(180deg, rgba(26,29,41,0.7), rgba(23,26,36,0.7));
        border: 1px solid #262838;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: left;
        height: 100%;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
    }
    .feature-icon {
        font-size: 1.6rem;
        margin-bottom: 10px;
    }
    .feature-title {
        font-weight: 700;
        font-size: 1rem;
        color: #F5F5F7;
        margin-bottom: 6px;
    }
    .feature-desc {
        color: #8B8D98;
        font-size: 0.85rem;
        line-height: 1.5;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---- Landing page (shown first, before entering the app) ----
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if not st.session_state.app_started:
    st.markdown('<div class="landing-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="landing-hero-title">🎤 AI Interview Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="landing-subtitle">Realistic, adaptive technical interviews personalized to each '
        'candidate\'s actual learning journey through the AI Cohort.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """<div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Personalized</div>
                <div class="feature-desc">Questions adapt to each candidate's real strengths and gaps.</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """<div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">Conversational</div>
                <div class="feature-desc">Natural follow-ups, not a static quiz. Feels like a real interview.</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """<div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">Actionable Feedback</div>
                <div class="feature-desc">A clear summary of strengths, gaps, and next steps at the end.</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1, 1])
    with mid:
        if st.button("Get Started →", type="primary", use_container_width=True):
            st.session_state.app_started = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="hero-title">🎤 AI Interview Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Personalized technical interviews, built for the AI Cohort</div>', unsafe_allow_html=True)

# ---- Load all candidates ----
# ---- Load all candidates ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "data", "candidates.json")) as f:
    all_candidates = json.load(f)["candidates"]

names = [f"{c['member']['name']} ({c['member']['id']})" for c in all_candidates]

# ---- Sidebar: candidate selection ----
with st.sidebar:
    st.markdown('<div class="sidebar-section-label">Select Candidate</div>', unsafe_allow_html=True)
    display_names = ["+ New Candidate"] + names
    selected_name = st.selectbox("Choose who to interview:", display_names, label_visibility="collapsed")

    if "active_new_candidate" not in st.session_state:
        st.session_state.active_new_candidate = None

    if selected_name == "+ New Candidate":
        if st.session_state.active_new_candidate is not None:
            selected_candidate = st.session_state.active_new_candidate
            st.caption(f"Currently interviewing: {selected_candidate['member']['name']}")
            if st.button("End this and pick someone else"):
                st.session_state.active_new_candidate = None
                st.session_state.current_candidate_id = None
                st.rerun()
        else:
            st.subheader("New Candidate Details")
            new_name = st.text_input("Full name")
            new_role = st.text_input("Job role")
            new_experience = st.number_input("Years of experience", min_value=0, max_value=50, value=0)
            start_clicked = st.button("Start Interview", type="primary")

            if not start_clicked:
                st.stop()

            if not new_name.strip() or not new_role.strip():
                st.error("Please enter both a name and a job role before starting.")
                st.stop()

            selected_candidate = {
                "member": {
                    "id": "NEW-" + new_name.replace(" ", "").upper(),
                    "name": new_name,
                    "jobRole": new_role,
                    "yearsExperience": new_experience,
                },
                "missions": [],
            }
            st.session_state.active_new_candidate = selected_candidate
    else:
        st.session_state.active_new_candidate = None
        selected_index = names.index(selected_name)
        selected_candidate = all_candidates[selected_index]

    m = selected_candidate["member"]
    st.markdown(
        f"""
        <div class="profile-card">
            <div class="profile-name">{m['name']}</div>
            <div class="profile-meta">{m.get('jobRole', 'N/A')} · {m.get('yearsExperience', '?')} yrs experience</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    missions = selected_candidate.get("missions", [])
    if missions:
        st.markdown('<div class="sidebar-section-label">Learning History</div>', unsafe_allow_html=True)
        for mission in missions:
            if mission.get("skipped"):
                continue
            css_class = "mission-struggled" if mission.get("passed") is False else "mission-strong"
            label = "Struggled" if mission.get("passed") is False else "Strong"
            st.markdown(
                f"""<div class="mission-badge {css_class}">
                    <span>{mission.get('title', 'Untitled')}</span>
                    <span>{label}</span>
                </div>""",
                unsafe_allow_html=True,
            )

# ---- Reset the interview whenever a different candidate is picked ----
if "current_candidate_id" not in st.session_state or st.session_state.current_candidate_id != selected_candidate["member"]["id"]:
    st.session_state.current_candidate_id = selected_candidate["member"]["id"]
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.done = False
    st.session_state.feedback = None

    with st.spinner("Preparing your interview..."):
        response = requests.post(BACKEND_URL, json={
            "sessionId": st.session_state.session_id,
            "candidate": selected_candidate,
        })
    data = response.json()
    st.session_state.messages.append({"role": "assistant", "content": data["reply"]})
    st.session_state.progress = data.get("progress", {"asked": 1, "min": 8})

# ---- Interview in progress: show progress bar + chat ----
if not st.session_state.done:
    if "progress" in st.session_state:
        p = st.session_state.progress
        st.caption(f"Question {p['asked']} of ~{p['min']}")
        st.progress(min(p["asked"] / p["min"], 1.0))

    for msg in st.session_state.messages:
        avatar = "🧑‍💼" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    user_input = st.chat_input("Type your answer...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            response = requests.post(BACKEND_URL, json={
                "sessionId": st.session_state.session_id,
                "message": user_input,
            })
        data = response.json()

        st.session_state.messages.append({"role": "assistant", "content": data["reply"]})

        if data.get("done"):
            st.session_state.done = True
            st.session_state.feedback = data.get("feedback")
        else:
            st.session_state.progress = data.get("progress", st.session_state.progress)

        st.rerun()

# ---- Interview complete: dedicated results screen ----
if st.session_state.done and st.session_state.feedback:
    fb = st.session_state.feedback

    st.markdown('<div class="results-screen">', unsafe_allow_html=True)
    st.markdown('<div class="results-title">📋 Interview Complete</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="results-subtitle">Results for {selected_candidate["member"]["name"]}</div>', unsafe_allow_html=True)

    st.markdown(
        f"""<div class="feedback-card feedback-summary" style="animation: fadeInUp 0.4s ease 0.05s both;">
            <div class="feedback-card-title">Summary</div>
            {fb.get('summary', '')}
        </div>""",
        unsafe_allow_html=True,
    )

    strengths_html = "".join(f"<li>{s}</li>" for s in fb.get("strengths", []))
    st.markdown(
        f"""<div class="feedback-card feedback-strengths" style="animation: fadeInUp 0.4s ease 0.15s both;">
            <div class="feedback-card-title">✅ Strengths</div>
            <ul>{strengths_html}</ul>
        </div>""",
        unsafe_allow_html=True,
    )

    gaps_html = "".join(f"<li>{g}</li>" for g in fb.get("gaps", []))
    st.markdown(
        f"""<div class="feedback-card feedback-gaps" style="animation: fadeInUp 0.4s ease 0.25s both;">
            <div class="feedback-card-title">⚠️ Gaps</div>
            <ul>{gaps_html}</ul>
        </div>""",
        unsafe_allow_html=True,
    )

    next_html = "".join(f"<li>{n}</li>" for n in fb.get("next", []))
    st.markdown(
        f"""<div class="feedback-card feedback-next" style="animation: fadeInUp 0.4s ease 0.35s both;">
            <div class="feedback-card-title">➡️ Next Steps</div>
            <ul>{next_html}</ul>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("View full transcript"):
        for msg in st.session_state.messages:
            role_label = "Interviewer" if msg["role"] == "assistant" else "Candidate"
            st.write(f"**{role_label}:** {msg['content']}")

    if st.button("🔄 Start New Interview", type="primary"):
        st.session_state.done = False
        st.session_state.feedback = None
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        with st.spinner("Preparing your interview..."):
            response = requests.post(BACKEND_URL, json={
                "sessionId": st.session_state.session_id,
                "candidate": selected_candidate,
            })
        data = response.json()
        st.session_state.messages.append({"role": "assistant", "content": data["reply"]})
        st.session_state.progress = data.get("progress", {"asked": 1, "min": 8})
        st.rerun()