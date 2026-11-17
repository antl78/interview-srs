META = {
    "title": "Index Of",
    "function": "index_of",
    "prompt": (
        "Renvoie l'indice de la première occurrence de `target` dans `items`, "
        "ou `-1` si `target` n'y est pas."
    ),
    "hints": [
        "`for i in range(len(items))` donne les indices.",
        "`items.index(target)` lève une `ValueError` si l'élément est absent.",
    ],
}


def index_of(items: list, target) -> int:
    """Reference solution."""
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1


TEST_CASES = [
    {"args": ([3, 7, 9], 7), "expected": 1},
    {"args": (["a", "b", "c"], "a"), "expected": 0},
    {"args": ([5, 2, 5], 5), "expected": 0, "note": "plusieurs occurrences : la première"},
    {"args": ([1, 2, 3], 4), "expected": -1, "note": "élément absent"},
    {"args": ([], 1), "expected": -1, "note": "liste vide"},
]
