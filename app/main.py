from parser.parser import parse_text
from parser.intent_detector import detect_intent
from frames.frame_engine import detect_frame
from frames.pass_engine import generate_pass
from evaluation.validator import validate_frame
from evaluation.scorer import score_evaluation
from output.formatter import format_output
from evaluation.pass_validator import validate_pass
from evaluation.feedback import generate_feedback
from evaluation.suggester import generate_suggestion
from concepts.concept_mapper import map_concepts

def run_pipeline(text):
    # L6 → Parsing
    parsed = parse_text(text)

    # L4 → Intent
    intent = detect_intent(parsed)

    # L5 → Frame
    frame = detect_frame(parsed)

    concepts = map_concepts(parsed)

    # 🔴 L4 → PASS GENERATION (NEW)
    cog_pass = generate_pass(intent, frame)

    # 🔴 NEW — PASS VALIDATION
    pass_validation = validate_pass(cog_pass, frame, intent)

    # L4 → Validation
    validation = validate_frame(frame, concepts)

    # L11 → Evaluation
    score = score_evaluation(validation, pass_validation)

    feedback = generate_feedback(validation, pass_validation, concepts)

    suggestion = generate_suggestion(parsed, intent, frame, pass_validation)

    # L6 → Output
    # attach
    result = {
        "input": text,
        "frame": frame,
        "validation": validation,
        "pass_validation": pass_validation,
        "score": score,
        "intent": intent,
        "pass": cog_pass,
        "feedback": feedback,
        "suggestion": suggestion,
        "concepts": concepts,
    }

    return format_output(result)

if __name__ == "__main__":
    print("=== COS Reasoning Evaluator v1 ===")
    user_input = input("Enter input: ")

    output = run_pipeline(user_input)
    print("\n--- OUTPUT ---")
    # print(output)
    print("\n".join(output))