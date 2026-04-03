def detect_frame(parsed):
    I = parsed.get("I")
    P = parsed.get("P")
    C = parsed.get("C")

    # 🔴 PRIORITY FIX: Cause first
    if I and C:
        return {
            "type": "cause",
            "pattern": ["I", "C"],
            "data": parsed,
            "valid": True
        }

    if I and P:
        return {
            "type": "description",
            "pattern": ["I", "P"],
            "data": parsed,
            "valid": True
        }

    return {
        "type": "unknown",
        "pattern": [],
        "data": parsed,
        "valid": False
    }