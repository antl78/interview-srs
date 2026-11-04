META = {
    "title": "Append to list",
    "function": "append_to_list",
    "prompt": (
        "Ajoute `item` à la fin de `items` et renvoie la liste. Si `items` "
        "n'est pas fourni, pars d'une nouvelle liste vide **à chaque appel**. "
        "Les cas de test appellent la fonction plusieurs fois de suite."
    ),
    "hints": [
        "Pourquoi ne pas écrire `items=[]` dans la signature ?",
        "La valeur par défaut est évaluée une seule fois, à la définition de la fonction.",
        "Crée la liste dans le corps : `if items is None: items = []`.",
    ],
}


def append_to_list(item: object, items: list | None = None) -> list:
    """Reference solution."""
    if items is None:
        items = []
    items.append(item)
    return items


TEST_CASES = [
    {"args": ("a",), "expected": ["a"]},
    {"args": ("b",), "expected": ["b"], "note": "2e appel sans liste : rien du 1er appel"},
    {"args": (3, [1, 2]), "expected": [1, 2, 3]},
    {"args": ("x",), "expected": ["x"], "note": "après un appel avec liste"},
    {"args": (0, []), "expected": [0], "note": "liste vide fournie"},
]
