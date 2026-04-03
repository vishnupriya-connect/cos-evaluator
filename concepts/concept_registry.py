# 🔴 GLOBAL REGISTRY (shared across functions)
_CONCEPTS = {
    "dog": {
        "type": "entity",
        "category": "animal",
        "can_do": ["run", "eat", "move"]
    },
    "plant": {
        "type": "entity",
        "category": "living",
        "can_do": ["grow"],
        "relations": {
            "needs": ["sunlight", "water"]
        }
    },
    "sunlight": {
        "type": "entity",
        "category": "natural_factor",
        "can_do": [],
        "relations": {
            "supports": ["plant"]
        }
    },
    "database": {
        "type": "entity",
        "category": "system",
        "can_do": []
    },
    "stone": {
        "type": "entity",
        "category": "non_living",
        "can_do": []
    }
}


def get_concept(word):
    return _CONCEPTS.get(word, None)


def get_vocabulary():
    return set(_CONCEPTS.keys())