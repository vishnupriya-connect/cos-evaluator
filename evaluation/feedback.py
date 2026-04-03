def generate_feedback(frame_validation, pass_validation):
    feedback = []

    errors = []
    errors.extend(frame_validation["errors"])
    errors.extend(pass_validation["errors"])

    # filter internal-only errors
    filtered_errors = []
    for err in errors:
        if "invalid pass generated" in err:
            continue
        filtered_errors.append(err)

    errors = filtered_errors

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

        # 🔴 INVALID FRAME
        elif "invalid frame" in err:
            feedback.append({
                "type": "structure",
                "message": "The sentence structure is incomplete or unclear."
            })

        # 🔴 CAUSE DIRECTION ERROR
        elif "invalid cause direction" in err:
            feedback.append({
                "type": "reasoning",
                "message": "Your cause and effect are reversed. Rewrite as: effect because cause."
            })

        # 🔴 GENERIC FALLBACK
        # else:
        #     feedback.append({
        #         "type": "general",
        #         "message": err
        #     })
        else:
            # Only show generic message if nothing else mapped
            feedback.append({
                "type": "general",
                "message": "The reasoning or structure needs improvement."
            })

    # remove duplicates
    unique_feedback = []
    seen = set()

    for item in feedback:
        msg = item["message"]
        if msg not in seen:
            seen.add(msg)
            unique_feedback.append(item)

    return unique_feedback