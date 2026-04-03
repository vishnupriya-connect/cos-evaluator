import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st

from parser.parser import parse_text
from parser.intent_detector import detect_intent
from frames.frame_engine import detect_frame
from frames.pass_engine import generate_pass
from evaluation.validator import validate_frame
from evaluation.pass_validator import validate_pass
from evaluation.scorer import score_evaluation
from evaluation.feedback import generate_feedback
from evaluation.suggester import generate_suggestion
from output.formatter import format_output


st.set_page_config(page_title="COS Reasoning Evaluator", layout="wide")

st.title("🧠 COS Reasoning Evaluator (v1)")

user_input = st.text_input("Enter your sentence:")

if st.button("Evaluate") and user_input:

    # PIPELINE
    parsed = parse_text(user_input)
    intent = detect_intent(parsed)
    frame = detect_frame(parsed)
    cog_pass = generate_pass(intent, frame)
    validation = validate_frame(frame)
    pass_validation = validate_pass(cog_pass, frame, intent)
    score = score_evaluation(validation, pass_validation)
    feedback = generate_feedback(validation, pass_validation)
    suggestion = generate_suggestion(parsed, intent, frame, pass_validation)

    result = {
        "input": user_input,
        "frame": frame,
        "validation": validation,
        "pass_validation": pass_validation,
        "score": score,
        "intent": intent,
        "pass": cog_pass,
        "feedback": feedback,
        "suggestion": suggestion
    }

    # DISPLAY

    # 🔴 SCORE (PRIMARY)
    st.metric("Final Score", score["final_score"])

    # 🔴 SUGGESTION (MOST IMPORTANT ACTION)
    if suggestion:
        st.subheader("Suggested Correction")
        st.success(suggestion)

    # 🔴 FEEDBACK (GUIDANCE)
    if feedback:
        st.subheader("Feedback")
        for f in feedback:
            st.write(f"- {f['message']}")

    # 🔴 DEBUG VIEW (COLLAPSIBLE)
    with st.expander("Show Detailed Analysis"):
        st.text(format_output(result))