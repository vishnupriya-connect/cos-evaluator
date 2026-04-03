def score_evaluation(frame_validation, pass_validation):
    errors = []
    errors.extend(frame_validation["errors"])
    errors.extend(pass_validation["errors"])

    frame_valid = frame_validation["is_valid"]
    pass_valid = pass_validation["is_valid"]

    # 🔴 TIER 1 — NO STRUCTURE → HARD FAIL
    if not frame_valid:
        # 🔴 distinguish structural vs concept failure
        has_concept_error = any("concept violation" in err for err in errors)

        if has_concept_error:
            return {
                "final_score": 0.2,
                "error_count": len(errors),
                "errors": errors
            }

        return {
            "final_score": 0.0,
            "error_count": len(errors),
            "errors": errors
        }

    # 🔴 TIER 2 — STRUCTURE OK, REASONING WRONG
    if frame_valid and not pass_valid:
        score = 0.5

        for err in errors:

            # 🔴 CONCEPT ERROR (HIGH IMPACT)
            if "concept violation" in err:
                score -= 0.5

            # 🔴 STRUCTURAL REASONING ERROR
            elif "invalid cause direction" in err:
                score -= 0.2

            # 🔴 GENERIC ERROR
            else:
                score -= 0.1

        if score < 0.0:
            score = 0.0

    # 🔴 TIER 3 — FULLY VALID
    return {
        "final_score": 1.0,
        "error_count": 0,
        "errors": []
    }