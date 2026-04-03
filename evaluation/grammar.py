def check_grammar(parsed):
    I = parsed.get("I")
    P = parsed.get("P")

    errors = []

    if I and P:
        entity = I[0]
        action = P[0]

        # simple rule: singular subject → verb should end with 's'
        if entity not in ["i", "you", "they"]:

            if not action.endswith("s"):
                errors.append(
                    f"grammar violation: '{entity}' should use '{action}s'"
                )

    return errors