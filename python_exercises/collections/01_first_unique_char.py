from collections import Counter

META = {
    "title": "First unique character",
    "function": "first_unique_char",
    "prompt": (
        "Renvoie l'indice du premier caractère de `text` qui n'apparaît qu'une "
        "seule fois, ou `-1` s'il n'y en a aucun. Le texte peut contenir "
        "200 000 caractères."
    ),
    "hints": [
        "Deux passes suffisent : compter d'abord, chercher ensuite.",
        "`text.count(c)` reparcourt tout le texte à chaque appel.",
        "`collections.Counter(text)` compte tout en une seule passe.",
    ],
}


def first_unique_char(text: str) -> int:
    """Reference solution."""
    counts = Counter(text)
    for index, char in enumerate(text):
        if counts[char] == 1:
            return index
    return -1


_LARGE_INPUT = "ab" * 100_000 + "c"

TEST_CASES = [
    {"args": ("leetcode",), "expected": 0},
    {"args": ("loveleetcode",), "expected": 2},
    {"args": ("aabb",), "expected": -1, "note": "aucun caractère unique"},
    {"args": ("",), "expected": -1, "note": "texte vide"},
    {"args": ("aA",), "expected": 0, "note": "majuscule et minuscule sont distinctes"},
    {"args": (_LARGE_INPUT,), "expected": 200_000, "note": "200 000 caractères (performance)"},
]
