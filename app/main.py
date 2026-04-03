from parser.parser import parse_text
from parser.intent_detector import detect_intent
from frames.frame_engine import detect_frame
from frames.pass_engine import generate_pass
from evaluation.validator import validate_frame
from evaluation.scorer import score_frame
from output.formatter import format_output
from evaluation.pass_validator import validate_pass
from evaluation.feedback import generate_feedback
from evaluation.suggester import generate_suggestion
from concepts.concept_mapper import map_concepts
from evaluation.grammar import check_grammar

def run_pipeline(text):
    # L6 → Parsing
    parsed = parse_text(text)
    grammar_errors = check_grammar(parsed)

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
        "grammar": grammar,
    }

    return format_output(result)

if __name__ == "__main__":
    print("=== COS Reasoning Evaluator v1 ===")
    user_input = input("Enter input: ")

    output = run_pipeline(user_input)
    print("\n--- OUTPUT ---")
    # print(output)
    print("\n".join(output))