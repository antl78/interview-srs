import copy

META = {
    "title": "History snapshots",
    "function": "history_snapshots",
    "prompt": (
        "`state` associe chaque joueur à la liste de ses points. Chaque coup de "
        "`moves` est un couple `(joueur, points)` : ajoute `points` à la liste du "
        "joueur (créée si besoin). Renvoie la liste des états après chaque coup ; "
        "chaque état reste figé, même après les coups suivants."
    ),
    "hints": [
        "Ajouter `state` à l'historique ajoute une référence, pas une photo.",
        "`dict.copy()` copie le dict, mais les listes à l'intérieur restent partagées.",
        "`copy.deepcopy` copie aussi les objets imbriqués.",
    ],
}


def history_snapshots(state: dict[str, list[int]], moves: list[tuple[str, int]]) -> list[dict[str, list[int]]]:
    """Reference solution."""
    current = copy.deepcopy(state)
    snapshots = []
    for player, points in moves:
        current.setdefault(player, []).append(points)
        snapshots.append(copy.deepcopy(current))
    return snapshots


TEST_CASES = [
    {"args": ({"ana": []}, [("ana", 3), ("ana", 5)]),
     "expected": [{"ana": [3]}, {"ana": [3, 5]}], "note": "copie superficielle insuffisante"},
    {"args": ({"ana": [1], "bob": []}, [("bob", 4), ("ana", 2)]),
     "expected": [{"ana": [1], "bob": [4]}, {"ana": [1, 2], "bob": [4]}]},
    {"args": ({}, [("ana", 1), ("bob", 2)]),
     "expected": [{"ana": [1]}, {"ana": [1], "bob": [2]}], "note": "joueur absent au départ"},
    {"args": ({"ana": [1]}, []), "expected": [], "note": "aucun coup"},
]
