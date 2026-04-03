def validate_frame(frame):
    errors = []
    data = frame.get("data", {})

    I = data.get("I")
    P = data.get("P")
    C = data.get("C")

    if not frame["valid"]:
        errors.append("invalid frame")

    if frame["type"] == "description":
        if not I:
            errors.append("missing entity (I)")
        if not P:
            errors.append("missing property/action (P)")

    if frame["type"] == "cause":
        if not I:
            errors.append("missing entity (I)")
        if not C:
            errors.append("missing cause (C)")

    # 🔴 HARD RULE: if entity missing → invalid
    if not I:
        errors.append("no valid entity detected")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }