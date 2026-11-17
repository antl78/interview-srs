META = {
    "title": "First And Last",
    "function": "first_and_last",
    "prompt": (
        "Renvoie un tuple `(premier, dernier)` avec le premier et le dernier "
        "élément de `items`. Lève une `ValueError` si la liste est vide."
    ),
    "hints": [
        "`items[-1]` est le dernier élément.",
        "Le résultat est un tuple : `(a, b)`, pas une liste `[a, b]`.",
    ],
}


def first_and_last(items: list) -> tuple:
    """Reference solution."""
    if not items:
        raise ValueError("empty list")
    return (items[0], items[-1])


TEST_CASES = [
    {"args": ([1, 2, 3, 4],), "expected": (1, 4)},
    {"args": (["a", "b"],), "expected": ("a", "b")},
    {"args": ([42],), "expected": (42, 42), "note": "un seul élément"},
    {"args": ([],), "raises": ValueError, "note": "liste vide"},
]
