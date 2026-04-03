def generate_pass(intent, frame):
    if not frame["valid"]:
        return {
            "type": "invalid_pass",
            "steps": [],
            "valid": False
        }

    data = frame.get("data", {})
    I = data.get("I")
    P = data.get("P")
    C = data.get("C")

    # 🔴 PASS TYPES BASED ON INTENT

    # DESCRIBE PASS
    if intent == "describe":
        return {
            "type": "describe_pass",
            "steps": [
                {"op": "identify_entity", "value": I},
                {"op": "identify_property", "value": P},
                {"op": "bind", "relation": "has_property"}
            ],
            "valid": True
        }

    # EXPLAIN PASS
    if intent == "explain":
        return {
            "type": "explain_pass",
            "steps": [
                {"op": "identify_entity", "value": I},
                {"op": "identify_cause", "value": C},
                {"op": "bind", "relation": "caused_by"}
            ],
            "valid": True
        }

    # ASSERT PASS
    if intent == "assert":
        return {
            "type": "assert_pass",
            "steps": [
                {"op": "identify_entity", "value": I},
                {"op": "confirm_existence"}
            ],
            "valid": True
        }

    return {
        "type": "unknown_pass",
        "steps": [],
        "valid": False
    }