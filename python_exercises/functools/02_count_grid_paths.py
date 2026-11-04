from functools import cache

META = {
    "title": "Count grid paths",
    "function": "count_grid_paths",
    "prompt": (
        "Dans une grille de `rows` × `cols` cases, on va de la case en haut à "
        "gauche à la case en bas à droite, en ne se déplaçant que vers la droite "
        "ou vers le bas. Renvoie le nombre de chemins possibles. Les cases de "
        "`blocked` (couples `(ligne, colonne)`) sont infranchissables. Une grille "
        "16 × 16 doit passer sous la limite de temps."
    ),
    "hints": [
        "Le nombre de chemins jusqu'à une case = chemins jusqu'à la case du dessus + jusqu'à celle de gauche.",
        "La récursion naïve recalcule les mêmes cases des millions de fois.",
        "`@functools.cache` sur une fonction interne `(ligne, colonne)` ; un `set` n'est pas hashable, garde-le hors des arguments mis en cache.",
    ],
}


def count_grid_paths(rows: int, cols: int, blocked: set[tuple[int, int]]) -> int:
    """Reference solution."""

    @cache
    def paths(row: int, col: int) -> int:
        if row < 0 or col < 0 or (row, col) in blocked:
            return 0
        if row == 0 and col == 0:
            return 1
        return paths(row - 1, col) + paths(row, col - 1)

    return paths(rows - 1, cols - 1)


TEST_CASES = [
    {"args": (2, 2, set()), "expected": 2},
    {"args": (3, 3, {(1, 1)}), "expected": 2, "note": "case centrale bloquée"},
    {"args": (1, 5, set()), "expected": 1, "note": "une seule ligne"},
    {"args": (3, 3, {(0, 0)}), "expected": 0, "note": "départ bloqué"},
    {"args": (3, 4, {(1, 1), (1, 2)}), "expected": 2},
    {"args": (16, 16, set()), "expected": 155_117_520, "note": "grille 16 × 16 (performance)"},
]
