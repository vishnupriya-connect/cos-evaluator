def parse_text(text):
    words = text.lower().split()

    parsed = {
        "I": [],
        "P": [],
        "C": None
    }

    verbs = {
        "is", "are", "runs", "run", "eats", "eat",
        "grows", "grow", "moves", "move",
        "flies", "fly", "works", "work"
    }

    cause_markers = {"because", "due", "since"}

    adverbs = {"quickly", "slowly", "fast"}

    i = 0
    while i < len(words):
        word = words[i]

        # CAUSE
        if word in cause_markers:
            parsed["C"] = " ".join(words[i+1:])
            break

        # VERB → P
        elif word in verbs:
            parsed["P"].append(word)

        # FILTER: ignore adverbs (do NOT treat as entity)
        elif word in adverbs:
            pass

        # ENTITY (basic noun assumption)
        else:
            parsed["I"].append(word)

        i += 1

    # cleanup
    if len(parsed["I"]) == 0:
        parsed["I"] = None
    if len(parsed["P"]) == 0:
        parsed["P"] = None

    return parsed