META = {
    "title": "Mean",
    "function": "mean",
    "prompt": (
        "Renvoie la moyenne arithmétique des nombres de `values`. "
        "Lève une `ValueError` si la liste est vide."
    ),
    "hints": ["sum() et len() suffisent ; attention à la division par zéro."],
}


def mean(values: list[float]) -> float:
    """Reference solution."""
    if not values:
        raise ValueError("mean of an empty list is undefined")
    return sum(values) / len(values)


TEST_CASES = [
    {"args": ([1, 2, 3, 4],), "expected": 2.5, "compare": "approx"},
    {"args": ([0.1, 0.2],), "expected": 0.15, "compare": "approx",
     "note": "arrondi des flottants"},
    {"args": ([5],), "expected": 5.0, "compare": "approx", "note": "une seule valeur"},
    {"args": ([],), "raises": ValueError, "note": "liste vide"},
]
