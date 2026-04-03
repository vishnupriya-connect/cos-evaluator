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
from main import *


st.set_page_config(page_title="COS Reasoning Evaluator", layout="wide")

st.title("🧠 COS Reasoning Evaluator (v1)")

user_input = st.text_input("Enter your sentence:")

if st.button("Evaluate") and user_input:

    # PIPELINE
    # parsed = parse_text(user_input)
    # intent = detect_intent(parsed)
    # frame = detect_frame(parsed)
    # cog_pass = generate_pass(intent, frame)
    # validation = validate_frame(frame)
    # pass_validation = validate_pass(cog_pass, frame, intent)
    # score = score_evaluation(validation, pass_validation)
    # feedback = generate_feedback(validation, pass_validation)
    # suggestion = generate_suggestion(parsed, intent, frame, pass_validation)

    # result = {
    #     "input": user_input,
    #     "frame": frame,
    #     "validation": validation,
    #     "pass_validation": pass_validation,
    #     "score": score,
    #     "intent": intent,
    #     "pass": cog_pass,
    #     "feedback": feedback,
    #     "suggestion": suggestion
    # }

    parsed = parse_text(user_input)
    grammar_errors = check_grammar(parsed)

    # L4 → Intent
    intent = detect_intent(parsed)

    # L5 → Frame
    frame = detect_frame(parsed)

    concepts = map_concepts(parsed)

    # 🔴 L4 → PASS GENERATION (NEW)
    cog_pass = generate_pass(intent, frame, concepts)

    # 🔴 NEW — PASS VALIDATION
    pass_validation = validate_pass(cog_pass, frame, intent)

    # L4 → Validation
    validation = validate_frame(frame, concepts)

   # keep grammar separate (do NOT merge into validation)
    grammar = {
        "is_valid": len(grammar_errors) == 0,
        "errors": grammar_errors
    }

    # L11 → Evaluation
    score = score_frame(frame["valid"],
                        pass_validation["is_valid"],
                        validation["errors"],
                        grammar["errors"]
                        )
    
    # 🔴 merge grammar errors ONLY for feedback (not for validation/scoring)
    combined_validation = {
        "errors": validation["errors"] + grammar["errors"]
    }

    feedback = generate_feedback(combined_validation, pass_validation, concepts)

    suggestion = generate_suggestion(frame, validation, concepts, grammar)

    # L6 → Output
    # attach
    result = {
        "input": user_input,
        "frame": frame,
        "validation": validation,
        "pass_validation": pass_validation,
        "score": score,
        "intent": intent,
        "pass": cog_pass,
        "feedback": feedback,
        "suggestion": suggestion,
        "concepts": concepts,
        "grammar": grammar,
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