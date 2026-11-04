META = {
    "title": "Strong password",
    "function": "is_strong_password",
    "prompt": (
        "Renvoie `True` si `password` contient au moins 8 caractères, au moins "
        "une majuscule et au moins un chiffre, `False` sinon."
    ),
    "hints": [
        "`any()` prend un générateur et s'arrête au premier élément vrai.",
        "`str.isupper()` et `str.isdigit()` gèrent aussi les lettres accentuées.",
    ],
}


def is_strong_password(password: str) -> bool:
    """Reference solution."""
    return (
        len(password) >= 8
        and any(char.isupper() for char in password)
        and any(char.isdigit() for char in password)
    )


TEST_CASES = [
    {"args": ("Secret123",), "expected": True},
    {"args": ("secret123",), "expected": False, "note": "pas de majuscule"},
    {"args": ("SecretPwd",), "expected": False, "note": "pas de chiffre"},
    {"args": ("Ab1",), "expected": False, "note": "trop court"},
    {"args": ("",), "expected": False, "note": "chaîne vide"},
    {"args": ("été2026Été",), "expected": True, "note": "majuscule accentuée"},
]
