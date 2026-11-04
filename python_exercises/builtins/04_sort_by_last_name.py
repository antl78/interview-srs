META = {
    "title": "Sort by last name",
    "function": "sort_by_last_name",
    "prompt": (
        "`names` contient des noms au format « Prénom Nom ». Renvoie-les triés "
        "par nom de famille, puis par prénom, sans tenir compte de la casse."
    ),
    "hints": [
        "`sorted()` accepte un paramètre `key` : une fonction appliquée à chaque élément.",
        "La clé peut renvoyer un tuple ou une liste : `(nom, prénom)` en minuscules.",
    ],
}


def sort_by_last_name(names: list[str]) -> list[str]:
    """Reference solution."""
    return sorted(names, key=lambda name: name.lower().split()[::-1])


TEST_CASES = [
    {"args": (["Ada Lovelace", "Alan Turing", "Grace Hopper"],),
     "expected": ["Grace Hopper", "Ada Lovelace", "Alan Turing"]},
    {"args": (["Marie Curie", "Pierre Curie", "Eve Curie"],),
     "expected": ["Eve Curie", "Marie Curie", "Pierre Curie"],
     "note": "même nom : départage par le prénom"},
    {"args": (["bob martin", "Alice Martin", "Zoe adams"],),
     "expected": ["Zoe adams", "Alice Martin", "bob martin"], "note": "casse mélangée"},
    {"args": ([],), "expected": [], "note": "liste vide"},
]
