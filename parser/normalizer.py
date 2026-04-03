from concepts.concept_registry import get_vocabulary
from concepts.spell_corrector import correct_word


def normalize_parsed(parsed):
    I = parsed.get("I")
    P = parsed.get("P")
    C = parsed.get("C")

    vocabulary = get_vocabulary()

    def normalize_word(word):
        if len(word) <= 3:
            return word

        protected = {"is", "was", "has", "this", "his"}
        if word in protected:
            return word

        if word.endswith("s"):
            word = word[:-1]

        word = correct_word(word, vocabulary)
        return word

    # normalize entity
    if I:
        parsed["I"] = [normalize_word(w) for w in I]

    # normalize cause
    if C:
        words = C.split()
        corrected_words = [correct_word(w, vocabulary) for w in words]
        parsed["C"] = " ".join(corrected_words)

    # 🔴 CRITICAL FIX
    return parsed