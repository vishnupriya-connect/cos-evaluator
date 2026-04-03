import streamlit as st
import requests
import os

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="COS Evaluator", layout="wide")

st.title("🧠 COS Reasoning Evaluator")
st.caption("Evaluate your answers based on logic, reasoning, and clarity — not just keywords.")

with st.expander("ℹ️ How to use"):
    st.write("""
    - Enter a simple sentence or answer
    - Click Evaluate
    - Review:
        ✔ Score (how correct your reasoning is)
        ✔ Suggestion (how to improve)
        ✔ Feedback (what went wrong)
    """)
st.subheader("💡 Try Examples")

example_cols = st.columns(3)

with example_cols[0]:
    if st.button("Valid Example"):
        st.session_state["example"] = "plant grows because sunlight"

with example_cols[1]:
    if st.button("Grammar Error"):
        st.session_state["example"] = "plant grow"

with example_cols[2]:
    if st.button("Logic Error"):
        st.session_state["example"] = "stone runs"

if "example" in st.session_state:
    user_input = st.session_state["example"]
    st.text_area("Example Loaded:", value=user_input, height=100)

# -----------------------
# INPUT SECTION
# -----------------------
st.subheader("✍️ Enter Your Answer")

user_input = st.text_area(
    "Enter your answer",
    height=120,
    label_visibility="collapsed"
)

debug = st.checkbox("Show Debug Info")

# -----------------------
# EVALUATION
# -----------------------
if st.button("Evaluate") and user_input:

    response = requests.post(
        f"{API_BASE}/evaluate",
        params={"debug": str(debug).lower()},
        json={"text": user_input}
    )

    data = response.json()

    st.divider()
    st.subheader("📊 Evaluation Result")

    # DEBUG MODE
    if debug:
        st.json(data)
    else:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric("Score", data.get("score"))

        with col2:
            if data.get("suggestion"):
                st.success(f"✔ Suggested: {data.get('suggestion')}")

        if data.get("feedback"):
            st.subheader("📝 Feedback")
            for f in data["feedback"]:
                st.write(f"- {f['message']}")
        else:
            st.success("✔ No issues detected")

# -----------------------
# HISTORY SECTION
# -----------------------
st.divider()
st.subheader("📜 Recent Evaluations")

try:
    res = requests.get(f"{API_BASE}/evaluations")
    history = res.json()

    for item in history.get("results", []):
        with st.container():
            st.write(f"**Input:** {item['input']}")
            st.write(f"Score: {item['score']} | Intent: {item['intent']}")
            st.divider()

except:
    st.info("History not available")

# -----------------------
# LOW SCORE INSIGHTS
# -----------------------
st.divider()
st.subheader("⚠️ Areas to Improve")

try:
    res = requests.get(f"{API_BASE}/evaluations/low-score")
    low_data = res.json()

    if low_data.get("results"):
        for item in low_data["results"]:
            st.write(f"❌ {item['input']} → Score: {item['score']}")
    else:
        st.success("✔ No weak answers found")

except:
    st.info("Insights not available")

st.divider()
st.caption("Unlike traditional tools, COS evaluates reasoning — not just words.")    