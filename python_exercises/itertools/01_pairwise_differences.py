from itertools import pairwise

META = {
    "title": "Pairwise differences",
    "function": "pairwise_differences",
    "prompt": (
        "Renvoie la liste des écarts entre chaque valeur de `values` et la "
        "précédente (`values[i] - values[i - 1]`)."
    ),
    "hints": [
        "Combien d'écarts pour `n` valeurs ?",
        "`values[i - 1]` avec `i = 0` ne lève pas d'erreur en Python…",
        "`itertools.pairwise` donne les couples de voisins.",
    ],
}


def pairwise_differences(values: list[int]) -> list[int]:
    """Reference solution."""
    return [b - a for a, b in pairwise(values)]


TEST_CASES = [
    {"args": ([1, 4, 9, 16],), "expected": [3, 5, 7]},
    {"args": ([5, 3],), "expected": [-2], "note": "écart négatif"},
    {"args": ([2, 2, 2],), "expected": [0, 0]},
    {"args": ([7],), "expected": [], "note": "une seule valeur"},
    {"args": ([],), "expected": [], "note": "liste vide"},
]
