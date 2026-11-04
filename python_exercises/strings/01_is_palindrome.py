META = {
    "title": "Is palindrome",
    "function": "is_palindrome",
    "prompt": (
        "Renvoie `True` si `text` est un palindrome, en ignorant la casse, les "
        "espaces et la ponctuation : seuls les lettres et les chiffres comptent."
    ),
    "hints": [
        "Nettoie d'abord la chaîne, compare ensuite.",
        "`str.isalnum()` et le slicing `[::-1]`.",
    ],
}


def is_palindrome(text: str) -> bool:
    """Reference solution."""
    cleaned = [char.lower() for char in text if char.isalnum()]
    return cleaned == cleaned[::-1]


TEST_CASES = [
    {"args": ("radar",), "expected": True},
    {"args": ("hello",), "expected": False},
    {"args": ("Esope reste ici et se repose",), "expected": True, "note": "espaces et casse"},
    {"args": ("A man, a plan, a canal: Panama!",), "expected": True, "note": "ponctuation"},
    {"args": ("",), "expected": True, "note": "chaîne vide"},
    {"args": ("ab, BA?c",), "expected": False, "note": "presque un palindrome"},
]
