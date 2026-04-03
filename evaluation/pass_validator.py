def validate_pass(cog_pass, frame, intent):
    errors = []

    if not cog_pass["valid"]:
        errors.append("invalid pass generated")
        return {
            "is_valid": False,
            "errors": errors
        }

    steps = cog_pass.get("steps", [])
    data = frame.get("data", {})

    I = data.get("I")
    P = data.get("P")
    C = data.get("C")

    # 🔴 RULE 1: intent-pass alignment
    if intent == "describe" and cog_pass["type"] != "describe_pass":
        errors.append("intent-pass mismatch (expected describe_pass)")

    if intent == "explain" and cog_pass["type"] != "explain_pass":
        errors.append("intent-pass mismatch (expected explain_pass)")

    if intent == "assert" and cog_pass["type"] != "assert_pass":
        errors.append("intent-pass mismatch (expected assert_pass)")

    # 🔴 RULE 2: dependency presence
    if cog_pass["type"] == "describe_pass":
        if not I or not P:
            errors.append("missing dependency for describe (I, P required)")

    if cog_pass["type"] == "explain_pass":
        if not I or not C:
            errors.append("missing dependency for explain (I, C required)")

    if cog_pass["type"] == "assert_pass":
        if not I:
            errors.append("missing entity for assert")

    # 🔴 RULE 3: step validation
    if len(steps) == 0:
        errors.append("empty pass steps")

    # 🔴 RULE 4: operation sanity
    allowed_ops = {
        "identify_entity",
        "identify_property",
        "identify_cause",
        "bind",
        "confirm_existence"
    }

    for step in steps:
        op = step.get("op")
        if op and op not in allowed_ops:
            errors.append(f"invalid operation: {op}")

    # 🔴 RULE 5: CAUSAL DIRECTION CHECK (critical)

    if cog_pass["type"] == "explain_pass":
        # if cause contains verb → likely reversed structure
        if isinstance(C, str):
            cause_words = C.split()

            # simple heuristic: if cause contains verb-like word
            verbs = {
                "is", "are", "runs", "run", "grows", "grow",
                "moves", "move", "works", "work"
            }

            for word in cause_words:
                if word in verbs:
                    errors.append("invalid cause direction (effect used as cause)")
                    break

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }