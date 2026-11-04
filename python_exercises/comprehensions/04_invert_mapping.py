META = {
    "title": "Invert mapping",
    "function": "invert_mapping",
    "prompt": (
        "Renvoie le dictionnaire inverse de `mapping` : les valeurs deviennent "
        "les clés et inversement. Lève une `ValueError` si deux clés ont la "
        "même valeur."
    ),
    "hints": [
        "Une dict comprehension s'écrit `{k: v for ...}` et parcourt `d.items()`.",
        "Une valeur en double écrase une clé sans erreur : compare les tailles.",
    ],
}


def invert_mapping(mapping: dict) -> dict:
    """Reference solution."""
    inverted = {value: key for key, value in mapping.items()}
    if len(inverted) != len(mapping):
        raise ValueError("duplicate values cannot be inverted")
    return inverted


TEST_CASES = [
    {"args": ({"a": 1, "b": 2},), "expected": {1: "a", 2: "b"}},
    {"args": ({"fr": "France", "it": "Italy"},), "expected": {"France": "fr", "Italy": "it"}},
    {"args": ({},), "expected": {}, "note": "dictionnaire vide"},
    {"args": ({"a": 1, "b": 2, "c": 1},), "raises": ValueError, "note": "valeurs en double"},
]
