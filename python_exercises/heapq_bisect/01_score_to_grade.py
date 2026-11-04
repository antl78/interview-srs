from bisect import bisect_right

META = {
    "title": "Score to grade",
    "function": "score_to_grade",
    "prompt": (
        "Convertis chaque note de `scores` (sur 100) en lettre : moins de 60 → "
        "`\"F\"`, de 60 à moins de 70 → `\"D\"`, de 70 à moins de 80 → `\"C\"`, "
        "de 80 à moins de 90 → `\"B\"`, 90 et plus → `\"A\"`."
    ),
    "hints": [
        "Une chaîne de `if` marche, mais les seuils forment une liste triée.",
        "`bisect` donne la position d'une valeur parmi les seuils, donc l'indice de la lettre.",
        "Une note pile sur un seuil : `bisect_left` ou `bisect_right` ?",
    ],
}


def score_to_grade(scores: list[float]) -> list[str]:
    """Reference solution."""
    breakpoints = [60, 70, 80, 90]
    grades = "FDCBA"
    return [grades[bisect_right(breakpoints, score)] for score in scores]


TEST_CASES = [
    {"args": ([33, 99, 77, 89, 100],), "expected": ["F", "A", "C", "B", "A"]},
    {"args": ([60, 70, 90],), "expected": ["D", "C", "A"], "note": "pile sur un seuil"},
    {"args": ([59.5],), "expected": ["F"], "note": "note décimale"},
    {"args": ([0],), "expected": ["F"], "note": "zéro"},
    {"args": ([],), "expected": [], "note": "liste vide"},
]
