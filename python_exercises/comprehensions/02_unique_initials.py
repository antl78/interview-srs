META = {
    "title": "Unique initials",
    "function": "unique_initials",
    "prompt": (
        "Renvoie l'ensemble (`set`) des initiales, en minuscules, des mots de "
        "`words`. Les chaînes vides sont ignorées."
    ),
    "hints": [
        "Les accolades donnent une set comprehension : `{expr for x in it}`.",
        "`w[0]` sur une chaîne vide lève une `IndexError` : filtre avec `if w`.",
    ],
}


def unique_initials(words: list[str]) -> set[str]:
    """Reference solution."""
    return {word[0].lower() for word in words if word}


TEST_CASES = [
    {"args": (["Apple", "avocado", "Banana"],), "expected": {"a", "b"}},
    {"args": (["sql", "python", "spark"],), "expected": {"s", "p"}},
    {"args": (["", "cat", ""],), "expected": {"c"}, "note": "chaînes vides"},
    {"args": (["Éric", "éclair"],), "expected": {"é"}, "note": "accents et casse"},
    {"args": ([],), "expected": set(), "note": "liste vide : set(), pas {}"},
]
