def validate_frame(frame, concepts):
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

        # 🔴 CONCEPT-AWARE VALIDATION
        if I and P:
            for concept_item in concepts:
                concept = concept_item.get("concept")
                word = concept_item.get("word")

                if concept:
                    allowed = concept.get("can_do", [])

                    def normalize_action(action):
                        # basic normalization (MVP level)
                        if action.endswith("s"):
                            return action[:-1]
                        return action

                    for action in P:
                        normalized = normalize_action(action)

                        if normalized not in allowed:
                            errors.append(
                                f"concept violation: '{word}' cannot perform '{action}'"
                            )
                            
    if frame["type"] == "cause":
        if not I:
            errors.append("missing entity (I)")
        if not C:
            errors.append("missing cause (C)")
            # 🔴 CONCEPT RELATION VALIDATION (L8)
    if I and C:
        cause_text = C.lower()

        for concept_item in concepts:
            word = concept_item.get("word")
            concept = concept_item.get("concept", {})

            relations = concept.get("relations", {})

            for rel, targets in relations.items():
                for target in targets:
                    if target in cause_text:
                        break
                else:
                    continue
                break
            else:
                errors.append(
                    f"weak relation: '{word}' has no known relation with '{cause_text}'"
                )

    # 🔴 HARD RULE: if entity missing → invalid
    if not I:
        errors.append("no valid entity detected")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }