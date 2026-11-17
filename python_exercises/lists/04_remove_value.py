META = {
    "title": "Remove Value",
    "function": "remove_value",
    "prompt": (
        "Renvoie une nouvelle liste contenant les éléments de `items` dans le "
        "même ordre, sans aucune occurrence de `value`."
    ),
    "hints": [
        "Pars d'une liste vide et `append` les éléments à garder.",
        "`list.remove(value)` ne retire que la première occurrence.",
    ],
}


def remove_value(items: list, value) -> list:
    """Reference solution."""
    result = []
    for item in items:
        if item != value:
            result.append(item)
    return result


TEST_CASES = [
    {"args": ([1, 2, 3], 2), "expected": [1, 3]},
    {"args": ([4, 1, 4, 4, 2], 4), "expected": [1, 2], "note": "plusieurs occurrences"},
    {"args": ([1, 2, 3], 9), "expected": [1, 2, 3], "note": "valeur absente"},
    {"args": ([7, 7], 7), "expected": [], "note": "tout est retiré"},
    {"args": ([], 1), "expected": [], "note": "liste vide"},
]
