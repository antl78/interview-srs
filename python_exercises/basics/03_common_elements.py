META = {
    "title": "Common elements",
    "function": "common_elements",
    "prompt": (
        "Renvoie la liste des éléments présents à la fois dans `a` et dans `b`, "
        "sans doublons. L'ordre du résultat n'a pas d'importance."
    ),
    "hints": ["L'opérateur & entre deux sets donne leur intersection."],
}


def common_elements(a: list[int], b: list[int]) -> list[int]:
    """Reference solution."""
    return list(set(a) & set(b))


TEST_CASES = [
    {"args": ([1, 2, 3, 4], [3, 4, 5]), "expected": [3, 4], "compare": "unordered"},
    {"args": ([1, 1, 2], [1, 1, 1]), "expected": [1], "compare": "unordered",
     "note": "doublons"},
    {"args": ([1, 2], [3, 4]), "expected": [], "compare": "unordered",
     "note": "aucun élément commun"},
    {"args": ([], [1, 2]), "expected": [], "compare": "unordered", "note": "liste vide"},
]
