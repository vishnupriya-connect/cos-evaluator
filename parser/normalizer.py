def normalize_parsed(parsed):
    I = parsed.get("I")
    P = parsed.get("P")
    C = parsed.get("C")

    def normalize_word(word):
        # do not normalize short words
        if len(word) <= 3:
            return word

        # do not normalize known verbs
        protected = {"is", "was", "has", "this", "his"}
        if word in protected:
            return word

        # plural → singular (simple rule)
        if word.endswith("s"):
            return word[:-1]

        return word

    # normalize entity
    if I:
        parsed["I"] = [normalize_word(w) for w in I]

    # normalize property/action
    if P:
        parsed["P"] = [normalize_word(w) for w in P]

    # normalize cause (string)
    if C:
        words = C.split()
        words = [normalize_word(w) for w in words]
        parsed["C"] = " ".join(words)

    return parsed