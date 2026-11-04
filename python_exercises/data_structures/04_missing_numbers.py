META = {
    "title": "Missing numbers",
    "function": "missing_numbers",
    "prompt": (
        "`numbers` contient des entiers compris entre 1 et `n`, avec "
        "d'éventuels doublons. Renvoie la liste triée des entiers de 1 à `n` "
        "absents de `numbers`. `n` peut valoir 100 000."
    ),
    "hints": [
        "Tester `i not in numbers` pour chaque `i` refait un parcours complet de la liste.",
        "Convertis `numbers` en `set` une seule fois, avant la boucle.",
    ],
}


def missing_numbers(numbers: list[int], n: int) -> list[int]:
    """Reference solution."""
    present = set(numbers)
    return [i for i in range(1, n + 1) if i not in present]


_LARGE_INPUT = [i for i in range(1, 100_001) if i % 1000 != 0]

TEST_CASES = [
    {"args": ([3, 1, 5], 5), "expected": [2, 4]},
    {"args": ([2, 4, 6], 6), "expected": [1, 3, 5]},
    {"args": ([1, 2, 3], 3), "expected": [], "note": "rien ne manque"},
    {"args": ([2, 2, 2], 3), "expected": [1, 3], "note": "doublons"},
    {"args": ([], 3), "expected": [1, 2, 3], "note": "liste vide"},
    {"args": (_LARGE_INPUT, 100_000), "expected": list(range(1000, 100_001, 1000)),
     "note": "n = 100 000 (performance)"},
]
