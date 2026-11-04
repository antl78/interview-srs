META = {
    "title": "Positions of",
    "function": "positions_of",
    "prompt": (
        "Renvoie la liste des indices où `target` apparaît dans `items`, "
        "dans l'ordre croissant (liste vide si `target` est absent)."
    ),
    "hints": [
        "`list.index` ne renvoie que la première occurrence, et lève une erreur si la valeur est absente.",
        "`enumerate(items)` donne les paires `(indice, valeur)`.",
    ],
}


def positions_of(items: list, target: object) -> list[int]:
    """Reference solution."""
    return [index for index, value in enumerate(items) if value == target]


TEST_CASES = [
    {"args": (["a", "b", "a", "c"], "a"), "expected": [0, 2]},
    {"args": ([5, 3, 5, 5], 5), "expected": [0, 2, 3]},
    {"args": ([1, 2], 3), "expected": [], "note": "valeur absente"},
    {"args": ([], 1), "expected": [], "note": "liste vide"},
    {"args": ([None, 0, None], None), "expected": [0, 2], "note": "cible None"},
]
