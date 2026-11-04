META = {
    "title": "Flatten deep",
    "function": "flatten_deep",
    "prompt": (
        "Renvoie un générateur qui produit, de gauche à droite, tous les "
        "éléments de `nested`, quelle que soit la profondeur des listes et "
        "tuples imbriqués. Les chaînes de caractères sont des éléments : on "
        "ne les découpe pas."
    ),
    "hints": [
        "Un élément est soit à produire tel quel, soit à aplatir à son tour.",
        "Un générateur récursif délègue à un autre générateur avec `yield from`.",
        "`isinstance(item, (list, tuple))` distingue les conteneurs des chaînes.",
    ],
}


def flatten_deep(nested: list):
    """Reference solution."""
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten_deep(item)
        else:
            yield item


def to_list(result, *args):
    if iter(result) is not result:
        raise TypeError(f"flatten_deep() doit renvoyer un générateur, pas un {type(result).__name__}")
    return list(result)


TEST_CASES = [
    {"args": ([1, [2, [3, [4]]], 5],), "then": to_list, "expected": [1, 2, 3, 4, 5]},
    {"args": ([[1, 2], (3, 4)],), "then": to_list, "expected": [1, 2, 3, 4]},
    {"args": ([],), "then": to_list, "expected": [], "note": "liste vide"},
    {"args": ([[[]], [], [[[]]]],), "then": to_list, "expected": [], "note": "listes vides imbriquées"},
    {
        "args": (["ab", ["cd", ("e", 1)]],),
        "then": to_list,
        "expected": ["ab", "cd", "e", 1],
        "note": "les chaînes ne sont pas découpées, les tuples si",
    },
]
