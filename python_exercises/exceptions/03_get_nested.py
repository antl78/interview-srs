META = {
    "title": "Get nested",
    "function": "get_nested",
    "prompt": (
        "Suis le chemin `path` (clés de dict ou indices de liste) dans `data` et "
        "renvoie la valeur trouvée, ou `default` si le chemin n'existe pas. "
        "Une valeur `None` présente dans les données est une vraie valeur."
    ),
    "hints": [
        "Quelles exceptions lève `x[key]` quand `x` est un dict, une liste, une chaîne ?",
        "Un seul `try` autour de la boucle, plusieurs exceptions dans un tuple.",
        "`.get(...) or default` confond « absent » et « présent mais faux ».",
    ],
}


def get_nested(data: object, path: list[str | int], default: object = None) -> object:
    """Reference solution."""
    current = data
    try:
        for key in path:
            current = current[key]
    except (KeyError, IndexError, TypeError):
        return default
    return current


_DATA = {"user": {"name": "Ana", "tags": ["admin", "dev"], "email": None}}

TEST_CASES = [
    {"args": (_DATA, ["user", "name"]), "expected": "Ana"},
    {"args": (_DATA, ["user", "tags", 1]), "expected": "dev"},
    {"args": (_DATA, ["user", "phone"], "?"), "expected": "?", "note": "clé absente"},
    {"args": (_DATA, ["user", "tags", 5], "?"), "expected": "?", "note": "indice hors limites"},
    {"args": (_DATA, ["user", "name", "first"], "?"), "expected": "?",
     "note": "chemin qui continue dans une chaîne"},
    {"args": (_DATA, ["user", "email"], "?"), "expected": None, "note": "valeur None présente"},
]
