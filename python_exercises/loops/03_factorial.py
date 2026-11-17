META = {
    "title": "Factorial",
    "function": "factorial",
    "prompt": (
        "Renvoie la factorielle de `n` (`5! = 5 × 4 × 3 × 2 × 1 = 120`), avec une "
        "boucle. Par convention, `0! = 1`. Lève une `ValueError` si `n` est négatif."
    ),
    "hints": [
        "Pour un produit, l'accumulateur part de 1, pas de 0.",
        "`raise ValueError(\"...\")` en tout début de fonction pour le cas négatif.",
    ],
}


def factorial(n: int) -> int:
    """Reference solution."""
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


TEST_CASES = [
    {"args": (5,), "expected": 120},
    {"args": (3,), "expected": 6},
    {"args": (1,), "expected": 1},
    {"args": (0,), "expected": 1, "note": "0! = 1"},
    {"args": (-2,), "raises": ValueError, "note": "nombre négatif"},
]
