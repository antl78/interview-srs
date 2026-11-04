from itertools import combinations

META = {
    "title": "Pairs with sum",
    "function": "pairs_with_sum",
    "prompt": (
        "Renvoie les couples d'indices `(i, j)`, avec `i < j`, tels que "
        "`numbers[i] + numbers[j] == target`, triés par `i` puis par `j`."
    ),
    "hints": [
        "Un élément ne peut pas faire la paire avec lui-même, et `(j, i)` est le même couple que `(i, j)`.",
        "`combinations` renvoie les paires sans répétition, dans l'ordre d'entrée.",
        "Combine-le avec `enumerate` pour garder les indices.",
    ],
}


def pairs_with_sum(numbers: list[int], target: int) -> list[tuple[int, int]]:
    """Reference solution."""
    return [
        (i, j)
        for (i, a), (j, b) in combinations(enumerate(numbers), 2)
        if a + b == target
    ]


TEST_CASES = [
    {"args": ([1, 2, 3, 4], 5), "expected": [(0, 3), (1, 2)]},
    {"args": ([2, 2, 2], 4), "expected": [(0, 1), (0, 2), (1, 2)], "note": "valeurs répétées"},
    {"args": ([3], 6), "expected": [], "note": "un élément ne s'additionne pas à lui-même"},
    {"args": ([-1, 1, 0], 0), "expected": [(0, 1)], "note": "négatifs"},
    {"args": ([], 0), "expected": [], "note": "liste vide"},
]
