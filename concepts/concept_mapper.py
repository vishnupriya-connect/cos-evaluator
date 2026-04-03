from concepts.concept_registry import get_concept, get_vocabulary
from concepts.spell_corrector import correct_word


def map_concepts(parsed):
    I = parsed.get("I")

    concepts = []

    if I:
        vocabulary = get_vocabulary()

        for word in I:
            corrected_word = correct_word(word, vocabulary)
            concept = get_concept(corrected_word)

            if concept:
                concepts.append({
                    "word": corrected_word,
                    "concept": concept,
                })

    return concepts