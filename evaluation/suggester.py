def generate_suggestion(parsed, intent, frame, pass_validation):
    data = frame.get("data", {})

    I = data.get("I")
    P = data.get("P")
    C = data.get("C")

    # 🔴 CASE 1 — INVALID STRUCTURE (no entity)
    if not I:
        if P:
            return "Add a subject: e.g., 'Something " + " ".join(P) + "'"
        return "Add a clear subject and action."

    # 🔴 CASE 2 — CAUSE DIRECTION ERROR
    errors = pass_validation.get("errors", [])
    for err in errors:
        if "invalid cause direction" in err:
            if I and C:
                return f"{C} because {' '.join(I)}"

    # 🔴 CASE 3 — ENTITY PRESENT BUT NO ACTION (GENERAL RULE)
    if I and not P and not C:
        return f"{' '.join(I)} <add action>"

    # 🔴 CASE 4 — MISSING CAUSE
    if intent == "explain" and not C:
        return f"{' '.join(I)} {' '.join(P) if P else ''} because <cause>"

    # 🔴 CASE 5 — VALID (no suggestion needed)
    return None