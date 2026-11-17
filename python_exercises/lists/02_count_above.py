META = {
    "title": "Count Above",
    "function": "count_above",
    "prompt": (
        "Renvoie le nombre d'éléments de `numbers` strictement supérieurs "
        "à `threshold`."
    ),
    "hints": [
        "Un compteur à 0, une boucle, un `if`.",
        "« Strictement » : une valeur égale au seuil ne compte pas.",
    ],
}


def count_above(numbers: list[int], threshold: int) -> int:
    """Reference solution."""
    count = 0
    for number in numbers:
        if number > threshold:
            count += 1
    return count


TEST_CASES = [
    {"args": ([1, 5, 8, 3], 4), "expected": 2},
    {"args": ([10, 20, 30], 0), "expected": 3},
    {"args": ([4, 4, 5], 4), "expected": 1, "note": "valeurs égales au seuil"},
    {"args": ([-5, -1, 0], -2), "expected": 2, "note": "nombres négatifs"},
    {"args": ([], 3), "expected": 0, "note": "liste vide"},
]
