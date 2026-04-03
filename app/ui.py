import streamlit as st
import requests

API_URL = "https://cos-evaluator.onrender.com/evaluate"

st.set_page_config(page_title="COS Evaluator", layout="wide")

st.title("🧠 COS Reasoning Evaluator")

user_input = st.text_area("Enter your answer:")

debug = st.checkbox("Show Debug Info")

if st.button("Evaluate") and user_input:

    params = {"debug": str(debug).lower()}

    response = requests.post(
        API_URL,
        params=params,
        json={"text": user_input}
    )

    data = response.json()

    # 🔴 DEBUG MODE
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