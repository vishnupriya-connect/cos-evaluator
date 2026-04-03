from concepts.concept_registry import get_concept


def map_concepts(parsed):
    I = parsed.get("I")

    concepts = []

    if I:
        for word in I:
            concept = get_concept(word)
            if concept:
                concepts.append({
                    "word": word,
                    "concept": concept
                })

    return concepts