def detect_intent(parsed):
    I = parsed.get("I")
    P = parsed.get("P")
    C = parsed.get("C")

    # 🔴 Priority order (important)

    # EXPLAIN → cause present
    if C:
        return "explain"

    # DESCRIBE → entity + property
    if I and P:
        return "describe"

    # ASSERT → only entity
    if I and not P and not C:
        return "assert"

    # UNKNOWN
    return "unknown"