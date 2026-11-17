META = {
    "title": "Sum To N",
    "function": "sum_to_n",
    "prompt": (
        "Renvoie la somme des entiers de 1 à `n` inclus, avec une boucle. "
        "Pour `n` égal à 0, la somme vaut 0."
    ),
    "hints": [
        "Initialise un total à 0 avant la boucle, puis ajoute chaque entier.",
        "`range(n)` s'arrête à `n - 1` : il faut `range(1, n + 1)`.",
    ],
}


def sum_to_n(n: int) -> int:
    """Reference solution."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


TEST_CASES = [
    {"args": (3,), "expected": 6},
    {"args": (10,), "expected": 55, "note": "n est inclus"},
    {"args": (1,), "expected": 1},
    {"args": (0,), "expected": 0, "note": "n = 0"},
]
