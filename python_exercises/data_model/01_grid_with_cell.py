META = {
    "title": "Grid with cell",
    "function": "grid_with_cell",
    "prompt": (
        "Crée une grille de `rows` lignes et `cols` colonnes remplie de `fill`, "
        "place `value` dans la case (`row`, `col`) et renvoie la grille (liste de "
        "listes). Une case hors de la grille lève une `IndexError`."
    ),
    "hints": [
        "Modifie une case, puis regarde les autres lignes.",
        "`[ligne] * rows` répète la même liste, pas des copies.",
        "Une compréhension crée une nouvelle liste à chaque tour.",
    ],
}


def grid_with_cell(rows: int, cols: int, fill: object, row: int, col: int, value: object) -> list[list]:
    """Reference solution."""
    grid = [[fill] * cols for _ in range(rows)]
    grid[row][col] = value
    return grid


TEST_CASES = [
    {"args": (3, 2, 0, 1, 0, 9), "expected": [[0, 0], [9, 0], [0, 0]],
     "note": "les autres lignes ne changent pas"},
    {"args": (2, 3, None, 1, 2, 1), "expected": [[None, None, None], [None, None, 1]]},
    {"args": (1, 1, ".", 0, 0, "#"), "expected": [["#"]], "note": "une seule case"},
    {"args": (2, 2, 0, 2, 0, 1), "raises": IndexError, "note": "case hors de la grille"},
]
