from bisect import bisect_left, bisect_right

META = {
    "title": "Count in ranges",
    "function": "count_in_ranges",
    "prompt": (
        "Pour chaque requête `(low, high)` de `queries`, compte les valeurs de "
        "`values` comprises entre `low` et `high` inclus (0 si `low > high`). "
        "`values` n'est pas triée ; jusqu'à 100 000 valeurs et 10 000 requêtes."
    ),
    "hints": [
        "Parcourir toutes les valeurs pour chaque requête est trop lent.",
        "Trie une seule fois, puis cherche les bornes par dichotomie.",
        "`bisect_right(ordered, high) - bisect_left(ordered, low)` ; vérifie le cas `low > high`.",
    ],
}


def count_in_ranges(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Reference solution."""
    ordered = sorted(values)
    return [
        max(0, bisect_right(ordered, high) - bisect_left(ordered, low))
        for low, high in queries
    ]


# Permutation de 0..99 999 (7919 est premier avec 100 000).
_LARGE_VALUES = [(i * 7919) % 100_000 for i in range(100_000)]
_LARGE_QUERIES = [(i * 9, i * 9 + 99) for i in range(10_000)]

TEST_CASES = [
    {"args": ([5, 1, 3, 3, 8], [(1, 3), (4, 10), (3, 3)]), "expected": [3, 2, 2]},
    {"args": ([3, 4, 5], [(5, 3)]), "expected": [0], "note": "low > high"},
    {"args": ([], [(0, 10)]), "expected": [0], "note": "aucune valeur"},
    {"args": ([1, 2], []), "expected": [], "note": "aucune requête"},
    {"args": (_LARGE_VALUES, _LARGE_QUERIES), "expected": [100] * 10_000,
     "note": "100 000 valeurs, 10 000 requêtes (performance)"},
]
