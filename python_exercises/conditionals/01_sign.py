META = {
    "title": "Sign",
    "function": "sign",
    "prompt": (
        "Renvoie `\"positive\"` si `n` est strictement positif, `\"negative\"` "
        "s'il est strictement négatif, et `\"zero\"` sinon."
    ),
    "hints": [
        "Trois cas : un `if`, un `elif` et un `else`.",
        "Zéro n'est ni positif ni négatif : il a son propre cas.",
    ],
}


def sign(n: int) -> str:
    """Reference solution."""
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


TEST_CASES = [
    {"args": (5,), "expected": "positive"},
    {"args": (-3,), "expected": "negative"},
    {"args": (0,), "expected": "zero", "note": "zéro"},
    {"args": (1,), "expected": "positive", "note": "juste au-dessus de zéro"},
    {"args": (-1,), "expected": "negative", "note": "juste en dessous de zéro"},
]
