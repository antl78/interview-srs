from collections import Counter

META = {
    "title": "Can build note",
    "function": "can_build_note",
    "prompt": (
        "Renvoie `True` si `note` peut s'écrire avec les caractères de "
        "`magazine`, chaque caractère du magazine ne servant qu'une fois. "
        "La casse compte."
    ),
    "hints": [
        "Ce n'est pas seulement une question de lettres présentes : combien de fois ?",
        "Deux `Counter` se comparent : `c1 <= c2` est vrai si chaque compte de `c1` est inférieur ou égal.",
    ],
}


def can_build_note(note: str, magazine: str) -> bool:
    """Reference solution."""
    return Counter(note) <= Counter(magazine)


TEST_CASES = [
    {"args": ("aa", "aab"), "expected": True},
    {"args": ("baa", "aab"), "expected": True},
    {"args": ("aa", "ab"), "expected": False, "note": "le nombre d'occurrences compte"},
    {"args": ("", "abc"), "expected": True, "note": "note vide"},
    {"args": ("abc", ""), "expected": False, "note": "magazine vide"},
    {"args": ("Ab", "ab"), "expected": False, "note": "casse"},
]
