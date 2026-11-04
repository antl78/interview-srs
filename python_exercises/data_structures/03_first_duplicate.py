META = {
    "title": "First duplicate",
    "function": "first_duplicate",
    "prompt": (
        "Parcours `items` de gauche à droite et renvoie le premier élément "
        "rencontré pour la deuxième fois, ou `None` s'il n'y a aucun doublon. "
        "La liste peut contenir 100 000 éléments."
    ),
    "hints": [
        "Garde en mémoire les éléments déjà vus.",
        "`x in list` parcourt toute la liste (O(n)) ; `x in set` est en O(1).",
    ],
}


def first_duplicate(items: list[int]) -> int | None:
    """Reference solution."""
    seen = set()
    for item in items:
        if item in seen:
            return item
        seen.add(item)
    return None


_LARGE_INPUT = list(range(100_000)) + [99_999]

TEST_CASES = [
    {"args": ([3, 1, 4, 1, 5],), "expected": 1},
    {"args": ([2, 5, 5, 2],), "expected": 5,
     "note": "premier doublon rencontré, pas premier élément répété"},
    {"args": ([1, 2, 3],), "expected": None, "note": "aucun doublon"},
    {"args": ([],), "expected": None, "note": "liste vide"},
    {"args": (_LARGE_INPUT,), "expected": 99_999, "note": "100 000 éléments (performance)"},
]
