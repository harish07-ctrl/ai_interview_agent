import streamlit as st
import json
import os

st.set_page_config(page_title="Host View", page_icon="🔒")
st.title("🔒 Host View — All Feedback")

log_path = "../backend/interview_log.json"


def load_log():
    if not os.path.exists(log_path):
        return []
    with open(log_path) as f:
        return json.load(f)


def save_log(log):
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)


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
log = load_log()

if not log:
    st.info("No interviews completed yet.")
else:
    if st.button("Delete ALL feedback", type="primary"):
        save_log([])
        st.rerun()

    st.divider()

    for i in reversed(range(len(log))):
        record = log[i]
        with st.expander(f"{record['candidate_name']} — {record['timestamp'][:19]}"):
            fb = record["feedback"]
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
                log.pop(i)
                save_log(log)
                st.rerun()