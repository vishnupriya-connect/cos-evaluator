def generate_suggestion(frame, validation, concepts):
    errors = validation.get("errors", [])

    if not errors:
        return None

    for err in errors:

        # 🔴 CONCEPT VIOLATION
        if "concept violation" in err:

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

            # ✅ CASE 1 — entity can do something → suggest valid action
            if allowed_actions:
                correct_action = allowed_actions[0]
                return f"{entity} {correct_action}"

            # ❌ CASE 2 — entity cannot perform any action → suggest rethink
            return f"Use an entity that can perform '{action}' (e.g., dog {action})"

    return None