def generate_suggestion(frame, validation, concepts, grammar):

    errors = validation.get("errors", [])

    grammar_errors = grammar.get("errors", [])

    # only return None if BOTH are empty
    if not errors and not grammar_errors:
        return None

    has_concept_error = any("concept violation" in e for e in errors)

    for err in errors:

        # 🔴 PRIORITY 1 — CONCEPT VIOLATION
        if has_concept_error:
            if "concept violation" not in err:
                continue

            try:
                parts = err.split("'")
                entity = parts[1]
                action = parts[3]
            except:
                return None

            # find concept
            concept_data = None
            for c in concepts:
                if c.get("word") == entity:
                    concept_data = c.get("concept", {})
                    break

            if not concept_data:
                return None

            allowed_actions = concept_data.get("can_do", [])

            if allowed_actions:
                return f"{entity} {allowed_actions[0]}"

            return f"Use an entity that can perform '{action}' (e.g., dog {action})"


    # 🔴 PRIORITY 2 — GRAMMAR FIX (ONLY if no concept error)
    for err in grammar.get("errors", []):
        if "grammar violation" in err:
            try:
                parts = err.split("'")
                entity = parts[1]
                correct = parts[3]
                return f"{entity} {correct}"
            except:
                return None
            
    return None