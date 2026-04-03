import streamlit as st
import requests

API_BASE = "https://cos-evaluator.onrender.com"

st.set_page_config(page_title="COS Evaluator", layout="wide")

st.title("🧠 COS Reasoning Evaluator")

# -----------------------
# MODE SELECTOR
# -----------------------
mode = st.radio("Mode", ["Single Input", "Batch Input"])

debug = st.checkbox("Show Debug Info")

# -----------------------
# SINGLE INPUT
# -----------------------
if mode == "Single Input":

    user_input = st.text_area("Enter your answer:")

    if st.button("Evaluate") and user_input:

        response = requests.post(
            f"{API_BASE}/evaluate",
            params={"debug": str(debug).lower()},
            json={"text": user_input}
        )

        data = response.json()

        if debug:
            st.subheader("Clean Output")
            st.json(data.get("clean"))

            st.subheader("Full Debug")
            st.json(data.get("debug"))

        else:
            st.metric("Score", data.get("score"))

            if data.get("suggestion"):
                st.success(data.get("suggestion"))

            if data.get("feedback"):
                st.subheader("Feedback")
                for f in data["feedback"]:
                    st.write(f"- {f['message']}")

# -----------------------
# BATCH INPUT
# -----------------------
if mode == "Batch Input":

    batch_input = st.text_area("Enter multiple lines (one per input):")

    if st.button("Evaluate Batch") and batch_input:

        lines = [l.strip() for l in batch_input.split("\n") if l.strip()]

        response = requests.post(
            f"{API_BASE}/evaluate-batch",
            params={"debug": str(debug).lower()},
            json={"texts": lines}
        )

        data = response.json()

        st.subheader("Batch Results")

        for item in data.get("results", []):
            if debug:
                st.json(item)
            else:
                st.write(f"**Input:** {item['input']}")
                st.write(f"Score: {item['score']} | Intent: {item['intent']}")
                st.divider()

# -----------------------
# STATS DASHBOARD
# -----------------------
st.divider()
st.subheader("📊 System Stats")

try:
    stats = requests.get(f"{API_BASE}/evaluations/stats").json()

    col1, col2 = st.columns(2)

    col1.metric("Total Evaluations", stats.get("total", 0))
    col2.metric("Average Score", stats.get("avg_score", 0))

    st.write("Intent Distribution:")
    for intent, count in stats.get("intent_distribution", []):
        st.write(f"- {intent}: {count}")

except:
    st.warning("Stats not available (Render reset or API issue)")

# -----------------------
# HISTORY PANEL
# -----------------------
st.divider()
st.subheader("📜 Recent Evaluations")

try:
    history = requests.get(f"{API_BASE}/evaluations").json()

    for item in history.get("results", []):
        st.write(f"**Input:** {item['input']}")
        st.write(f"Score: {item['score']} | Intent: {item['intent']}")
        st.divider()

except:
    st.warning("History not available")