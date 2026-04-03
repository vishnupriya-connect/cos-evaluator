def score_evaluation(frame_validation, pass_validation):
    errors = []
    errors.extend(frame_validation["errors"])
    errors.extend(pass_validation["errors"])

    frame_valid = frame_validation["is_valid"]
    pass_valid = pass_validation["is_valid"]

    # 🔴 TIER 1 — NO STRUCTURE → HARD FAIL
    if not frame_valid:
        return {
            "final_score": 0.0,
            "error_count": len(errors),
            "errors": errors
        }

    # 🔴 TIER 2 — STRUCTURE OK, REASONING WRONG
    if frame_valid and not pass_valid:
        score = 0.5

        # critical reasoning errors → reduce but NOT zero
        for err in errors:
            if "invalid cause direction" in err:
                score -= 0.2

        score -= 0.1 * len(errors)

        if score < 0.2:
            score = 0.2  # floor (important)

        return {
            "final_score": round(score, 2),
            "error_count": len(errors),
            "errors": errors
        }

    # 🔴 TIER 3 — FULLY VALID
    return {
        "final_score": 1.0,
        "error_count": 0,
        "errors": []
    }