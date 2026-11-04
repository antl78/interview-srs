META = {
    "title": "Dot product",
    "function": "dot_product",
    "prompt": (
        "Renvoie le produit scalaire de `a` et `b` (somme des produits terme "
        "à terme). Lève une `ValueError` si les listes n'ont pas la même longueur."
    ),
    "hints": [
        "`zip` parcourt deux listes en parallèle.",
        "`zip` s'arrête sans rien dire à la plus courte : regarde son paramètre `strict`.",
    ],
}


def dot_product(a: list[int], b: list[int]) -> int:
    """Reference solution."""
    return sum(x * y for x, y in zip(a, b, strict=True))


TEST_CASES = [
    {"args": ([1, 2, 3], [4, 5, 6]), "expected": 32},
    {"args": ([2], [3]), "expected": 6},
    {"args": ([-1, 2], [3, -4]), "expected": -11, "note": "nombres négatifs"},
    {"args": ([], []), "expected": 0, "note": "listes vides"},
    {"args": ([1, 2, 3], [1, 2]), "raises": ValueError, "note": "longueurs différentes"},
]
