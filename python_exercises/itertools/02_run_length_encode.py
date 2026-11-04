from itertools import groupby

META = {
    "title": "Run-length encoding",
    "function": "run_length_encode",
    "prompt": (
        "Compresse `text` en liste de couples `(caractère, nombre de répétitions "
        "consécutives)`. Exemple : `\"aaab\"` donne `[(\"a\", 3), (\"b\", 1)]`."
    ),
    "hints": [
        "Il s'agit de répétitions consécutives, pas d'un comptage global.",
        "`itertools.groupby` regroupe les éléments consécutifs égaux.",
        "Le groupe renvoyé est un itérateur : `len()` ne marche pas directement dessus.",
    ],
}


def run_length_encode(text: str) -> list[tuple[str, int]]:
    """Reference solution."""
    return [(char, sum(1 for _ in group)) for char, group in groupby(text)]


TEST_CASES = [
    {"args": ("aaabcc",), "expected": [("a", 3), ("b", 1), ("c", 2)]},
    {"args": ("aabaa",), "expected": [("a", 2), ("b", 1), ("a", 2)],
     "note": "un caractère peut revenir plus loin"},
    {"args": ("x",), "expected": [("x", 1)], "note": "un seul caractère"},
    {"args": ("",), "expected": [], "note": "texte vide"},
    {"args": ("aA",), "expected": [("a", 1), ("A", 1)], "note": "casse"},
]
