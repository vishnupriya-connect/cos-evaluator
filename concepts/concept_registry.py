def get_concept(word):
    registry = {
        "dog": {
            "type": "entity",
            "category": "animal",
            "can_do": ["run", "eat", "move"]
        },
        "plant": {
            "type": "entity",
            "category": "living",
            "can_do": ["grow"]
        },
        "sunlight": {
            "type": "entity",
            "category": "natural_factor",
            "can_do": []
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

    return registry.get(word, None)