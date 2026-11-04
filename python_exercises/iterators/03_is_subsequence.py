META = {
    "title": "Is subsequence",
    "function": "is_subsequence",
    "prompt": (
        "Renvoie `True` si les éléments de `sub` apparaissent dans `seq` "
        "dans le même ordre, pas forcément côte à côte (`\"ace\"` est une "
        "sous-séquence de `\"abcde\"`, pas `\"aec\"`). Chaque élément de "
        "`seq` ne sert qu'une fois."
    ),
    "hints": [
        "`x in seq` cherche depuis le début à chaque fois : l'ordre est perdu.",
        "Un itérateur, lui, reprend là où il s'était arrêté.",
        "`it = iter(seq)` puis `all(x in it for x in sub)` : `in` consomme `it`.",
    ],
}


def is_subsequence(sub, seq) -> bool:
    """Reference solution."""
    it = iter(seq)
    return all(x in it for x in sub)


TEST_CASES = [
    {"args": ("ace", "abcde"), "expected": True},
    {"args": ([1, 3], [1, 2, 3]), "expected": True},
    {"args": ("aec", "abcde"), "expected": False, "note": "bons éléments, mauvais ordre"},
    {"args": ("aa", "a"), "expected": False, "note": "un élément de seq ne sert qu'une fois"},
    {"args": ("", "abc"), "expected": True, "note": "sous-séquence vide"},
    {"args": ("a", ""), "expected": False, "note": "séquence vide"},
]
