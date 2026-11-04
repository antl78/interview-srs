META = {
    "title": "Word frequencies",
    "function": "word_frequencies",
    "prompt": (
        "Renvoie un dictionnaire qui associe à chaque mot de `text` son nombre "
        "d'occurrences. Le comptage est insensible à la casse ; les mots sont "
        "séparés par un ou plusieurs espaces."
    ),
    "hints": [
        "`counts[word] += 1` lève une `KeyError` la première fois.",
        "`dict.get(clé, 0)` renvoie 0 si la clé est absente.",
    ],
}


def word_frequencies(text: str) -> dict[str, int]:
    """Reference solution."""
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


TEST_CASES = [
    {"args": ("a b a",), "expected": {"a": 2, "b": 1}},
    {"args": ("le chat et le chien",), "expected": {"le": 2, "chat": 1, "et": 1, "chien": 1}},
    {"args": ("Data data DATA",), "expected": {"data": 3}, "note": "casse"},
    {"args": ("  x   y  ",), "expected": {"x": 1, "y": 1}, "note": "espaces multiples"},
    {"args": ("",), "expected": {}, "note": "texte vide"},
]
