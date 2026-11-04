META = {
    "title": "Capitalize words",
    "function": "capitalize_words",
    "prompt": (
        "Met en majuscule la première lettre de chaque mot de `text` (mots "
        "séparés par des espaces), sans modifier les autres lettres. Les "
        "espaces sont conservés tels quels."
    ),
    "hints": [
        "Méfie-toi de `str.title()` et de `str.capitalize()` : teste-les sur « l'école » et « iPhone ».",
        "`text.split(\" \")` garde les espaces multiples (chaînes vides), contrairement à `split()`.",
        "`word[:1].upper() + word[1:]` ne plante pas sur un mot vide.",
    ],
}


def capitalize_words(text: str) -> str:
    """Reference solution."""
    return " ".join(word[:1].upper() + word[1:] for word in text.split(" "))


TEST_CASES = [
    {"args": ("hello world",), "expected": "Hello World"},
    {"args": ("l'école est finie",), "expected": "L'école Est Finie",
     "note": "apostrophe (title() échoue)"},
    {"args": ("my iPhone",), "expected": "My IPhone",
     "note": "reste du mot inchangé (capitalize() échoue)"},
    {"args": ("well-known fact",), "expected": "Well-known Fact", "note": "trait d'union"},
    {"args": ("  two  spaces",), "expected": "  Two  Spaces", "note": "espaces multiples conservés"},
    {"args": ("",), "expected": "", "note": "chaîne vide"},
]
