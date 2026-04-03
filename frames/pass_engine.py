def generate_pass(intent, frame, concepts):
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

        steps = [
            {"op": "identify_entity", "value": I},
            {"op": "identify_cause", "value": C}
        ]

        relation_found = False

        if I and C:
            cause_text = C.lower()

            for concept_item in concepts:
                word = concept_item.get("word")
                concept = concept_item.get("concept", {})

                if word in I:
                    relations = concept.get("relations", {})

                    for rel, targets in relations.items():
                        if any(target in cause_text for target in targets):
                            steps.append({
                                "op": "bind",
                                "relation": rel
                            })
                            relation_found = True
                            break

        # 🔴 fallback
        if not relation_found:
            steps.append({
                "op": "bind",
                "relation": "caused_by"
            })

        return {
            "type": "explain_pass",
            "steps": steps,
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