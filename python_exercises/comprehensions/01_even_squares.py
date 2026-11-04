META = {
    "title": "Even squares",
    "function": "even_squares",
    "prompt": (
        "Renvoie la liste des carrés des nombres **pairs** de `numbers`, "
        "dans leur ordre d'apparition."
    ),
    "hints": [
        "Une list comprehension accepte un `if` à la fin : `[expr for x in it if cond]`.",
        "Teste la parité avec `n % 2 == 0`, pas avec la truthiness de `n`.",
    ],
}


def even_squares(numbers: list[int]) -> list[int]:
    """Reference solution."""
    return [n * n for n in numbers if n % 2 == 0]


TEST_CASES = [
    {"args": ([1, 2, 3, 4],), "expected": [4, 16]},
    {"args": ([6, 5, 2],), "expected": [36, 4]},
    {"args": ([-2, -3, 0],), "expected": [4, 0], "note": "négatifs et zéro (0 est pair)"},
    {"args": ([1, 3, 5],), "expected": [], "note": "aucun nombre pair"},
    {"args": ([],), "expected": [], "note": "liste vide"},
]
