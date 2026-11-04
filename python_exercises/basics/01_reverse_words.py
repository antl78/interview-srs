META = {
    "title": "Reverse words",
    "function": "reverse_words",
    "prompt": (
        "Renvoie la phrase `sentence` avec ses mots dans l'ordre inverse. "
        "Les mots sont séparés par un ou plusieurs espaces ; le résultat les "
        "sépare par un seul espace, sans espace au début ni à la fin."
    ),
    "hints": [
        "str.split() sans argument découpe sur n'importe quelle suite d'espaces.",
        "Le slicing [::-1] inverse une liste.",
    ],
}


def reverse_words(sentence: str) -> str:
    """Reference solution."""
    return " ".join(sentence.split()[::-1])


TEST_CASES = [
    {"args": ("hello world",), "expected": "world hello"},
    {"args": ("one two three",), "expected": "three two one"},
    {"args": ("  spaced   out  ",), "expected": "out spaced", "note": "espaces multiples"},
    {"args": ("single",), "expected": "single", "note": "un seul mot"},
    {"args": ("",), "expected": "", "note": "chaîne vide"},
]
