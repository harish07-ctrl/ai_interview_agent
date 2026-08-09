"""
Shared visual styling for every page.
Import get_custom_css() and pass it to st.markdown(..., unsafe_allow_html=True)
at the top of every page so the whole app looks consistent.
"""


def get_custom_css():
    return """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 820px;
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
    ::-webkit-scrollbar-thumb { background: #2D2F3D; border-radius: 8px; }
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
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .section-label {
        text-transform: uppercase;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #6B6D7A;
        margin: 20px 0 10px 0;
    }
    .profile-card, .stat-card, .row-card {
        background: linear-gradient(180deg, rgba(26,29,41,0.85), rgba(23,26,36,0.85));
        border: 1px solid #262838;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .profile-name, .row-title { font-size: 1.05rem; font-weight: 700; color: #F5F5F7; letter-spacing: -0.01em; }
    .profile-meta, .row-meta { color: #8B8D98; font-size: 0.85rem; margin-top: 2px; }
    .mission-badge {
        display: flex; justify-content: space-between; align-items: center;
        padding: 8px 12px; border-radius: 8px; margin-bottom: 6px;
        font-size: 0.8rem; font-weight: 500;
    }
    .mission-struggled { background: rgba(248,113,113,0.08); color: #F87171; border: 1px solid rgba(248,113,113,0.18); }
    .mission-strong { background: rgba(74,222,128,0.08); color: #4ADE80; border: 1px solid rgba(74,222,128,0.18); }
    .stat-number { font-size: 1.8rem; font-weight: 800; color: #F5F5F7; }
    .stat-label { color: #8B8D98; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
    [data-testid="stChatMessage"] { border-radius: 16px; padding: 6px 10px; margin-bottom: 10px; }
    .stButton > button { border-radius: 10px; font-weight: 600; border: none; transition: transform 0.15s ease; }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(99,102,241,0.3); }
    .stProgress > div > div > div { border-radius: 8px; background: linear-gradient(90deg, #6366F1, #A855F7); }
    .feedback-card { border-radius: 14px; padding: 18px 22px; margin-bottom: 16px; border: 1px solid; box-shadow: 0 2px 10px rgba(0,0,0,0.15); }
    .feedback-summary { background: rgba(99,102,241,0.14); border-color: rgba(99,102,241,0.3); }
    .feedback-strengths { background: rgba(34,197,94,0.14); border-color: rgba(34,197,94,0.3); }
    .feedback-gaps { background: rgba(245,158,11,0.14); border-color: rgba(245,158,11,0.3); }
    .feedback-next { background: rgba(59,130,246,0.14); border-color: rgba(59,130,246,0.3); }
    .feedback-card-title { font-weight: 700; font-size: 0.9rem; margin-bottom: 10px; }
    hr { border-color: #22242F !important; margin: 1.5rem 0 !important; }
</style>
"""