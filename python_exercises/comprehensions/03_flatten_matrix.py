META = {
    "title": "Flatten matrix",
    "function": "flatten_matrix",
    "prompt": (
        "Aplatis `matrix` (une liste de listes) en une seule liste, ligne par "
        "ligne. Les lignes peuvent être de longueurs différentes ou vides. "
        "Un seul niveau est aplati."
    ),
    "hints": [
        "Une comprehension peut contenir deux `for`.",
        "Les `for` s'écrivent dans le même ordre que des boucles imbriquées : "
        "`[x for row in matrix for x in row]`.",
    ],
}


def flatten_matrix(matrix: list[list]) -> list:
    """Reference solution."""
    return [value for row in matrix for value in row]


TEST_CASES = [
    {"args": ([[1, 2], [3, 4]],), "expected": [1, 2, 3, 4]},
    {"args": ([[1, 2, 3], [4], [5, 6]],), "expected": [1, 2, 3, 4, 5, 6],
     "note": "lignes de longueurs différentes"},
    {"args": ([[], [1], []],), "expected": [1], "note": "lignes vides"},
    {"args": ([],), "expected": [], "note": "matrice vide"},
    {"args": ([[[1], [2]], [[3]]],), "expected": [[1], [2], [3]],
     "note": "un seul niveau aplati"},
]
