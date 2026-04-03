def generate_feedback(frame_validation, pass_validation, concepts):
    feedback = []

    # collect all errors
    errors = []
    errors.extend(frame_validation.get("errors", []))
    errors.extend(pass_validation.get("errors", []))

    # filter internal-only errors
    filtered_errors = []
    for err in errors:
        if "invalid pass generated" in err:
            continue
        filtered_errors.append(err)

    errors = filtered_errors

    # 🔴 if no errors → no feedback
    if not errors:
        return []

    # process each error
    for err in errors:

        # 🔴 ENTITY MISSING
        if "missing entity" in err or "no valid entity" in err:
            feedback.append({
                "type": "structure",
                "message": "Add a clear subject (entity) to your sentence."
            })

        # 🔴 PROPERTY MISSING
        elif "missing property" in err:
            feedback.append({
                "type": "structure",
                "message": "Add an action or property to describe the entity."
            })

        # 🔴 CAUSE MISSING
        elif "missing cause" in err:
            feedback.append({
                "type": "reasoning",
                "message": "Provide a cause or reason for the statement."
            })

        # 🔴 CONCEPT-AWARE FEEDBACK
        elif "concept violation" in err:

            # extract entity + action
            try:
                parts = err.split("'")
                entity = parts[1]
                action = parts[3]
            except:
                entity = "this entity"
                action = "this action"

            # find concept category
            category = None
            for c in concepts:
                if c.get("word") == entity:
                    concept = c.get("concept", {})
                    category = concept.get("category")
                    break

            if category:
                message = f"'{entity}' is {category}, so it cannot perform '{action}'."
            else:
                message = f"'{entity}' cannot perform '{action}' based on its nature."

            feedback.append({
                "type": "semantic",
                "message": message
            })

        # 🔴 CAUSE DIRECTION ERROR
        elif "invalid cause direction" in err:
            feedback.append({
                "type": "reasoning",
                "message": "Your cause and effect are reversed. Rewrite as: effect because cause."
            })

        # 🔴 OTHER ERRORS → ignore (no noisy fallback here)
        else:
            pass

    # remove duplicate messages
    unique_feedback = []
    seen = set()

    for item in feedback:
        msg = item["message"]
        if msg not in seen:
            seen.add(msg)
            unique_feedback.append(item)

    # 🔴 fallback only if errors exist but none mapped
    if not unique_feedback:
        unique_feedback.append({
            "type": "general",
            "message": "The sentence needs improvement."
        })

    return unique_feedback