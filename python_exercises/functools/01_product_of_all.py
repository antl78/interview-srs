import operator
from functools import reduce

META = {
    "title": "Product of all",
    "function": "product_of_all",
    "prompt": "Renvoie le produit des nombres de `numbers`, et `1` si la liste est vide.",
    "hints": [
        "Que vaut le produit d'une liste vide, et pourquoi 1 ?",
        "`functools.reduce` accepte une valeur initiale en troisième argument.",
        "`operator.mul` évite d'écrire `lambda a, b: a * b` (et `math.prod` existe aussi).",
    ],
}


def product_of_all(numbers: list[float]) -> float:
    """Reference solution."""
    return reduce(operator.mul, numbers, 1)


TEST_CASES = [
    {"args": ([2, 3, 4],), "expected": 24},
    {"args": ([],), "expected": 1, "note": "liste vide"},
    {"args": ([5],), "expected": 5, "note": "un seul nombre"},
    {"args": ([3, 0, 2],), "expected": 0, "note": "un zéro"},
    {"args": ([-2, 3],), "expected": -6, "note": "négatif"},
    {"args": ([1.5, 2],), "expected": 3.0, "compare": "approx", "note": "flottants"},
]
