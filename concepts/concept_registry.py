def get_concept(word):
    registry = {
        "dog": {
            "type": "entity",
            "category": "animal"
        },
        "plant": {
            "type": "entity",
            "category": "living"
        },
        "sunlight": {
            "type": "entity",
            "category": "natural_factor"
        },
        "database": {
            "type": "entity",
            "category": "system"
        }
    }

    return registry.get(word, None)