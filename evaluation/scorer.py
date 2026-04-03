def score_frame(frame_valid, pass_valid, errors, grammar_errors):

    # 🔴 structural failure → worst
    if not frame_valid:
        return {
            "final_score": 0.0,
            "error_count": len(errors),
            "errors": errors
        }

    score = 1.0

    # 🔴 concept / reasoning errors (major)
    for err in errors:
        if "concept violation" in err:
            score -= 0.7
        elif "invalid cause direction" in err:
            score -= 0.3
        else:
            score -= 0.2

    # 🔴 grammar errors (minor)
    for err in grammar_errors:
        score -= 0.2

    if score < 0.0:
        score = 0.0

    return {
        "final_score": round(score, 2),
        "error_count": len(errors) + len(grammar_errors),
        "errors": errors + grammar_errors
    }