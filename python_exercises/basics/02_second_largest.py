META = {
    "title": "Second largest",
    "function": "second_largest",
    "prompt": (
        "Renvoie la deuxième plus grande valeur **distincte** de la liste "
        "`numbers`. Lève une `ValueError` s'il y a moins de deux valeurs "
        "distinctes."
    ),
    "hints": [
        "Les doublons ne comptent qu'une fois : pense au set.",
        "Une solution en un seul parcours, sans tri, est possible.",
    ],
}


def second_largest(numbers: list[int]) -> int:
    """Reference solution."""
    distinct = set(numbers)
    if len(distinct) < 2:
        raise ValueError("at least two distinct values are required")
    distinct.remove(max(distinct))
    return max(distinct)


TEST_CASES = [
    {"args": ([3, 1, 4, 1, 5],), "expected": 4},
    {"args": ([10, 10, 9],), "expected": 9, "note": "doublon du maximum"},
    {"args": ([-2, -5, -1],), "expected": -2, "note": "nombres négatifs"},
    {"args": ([7, 7, 7],), "raises": ValueError, "note": "une seule valeur distincte"},
    {"args": ([],), "raises": ValueError, "note": "liste vide"},
]
