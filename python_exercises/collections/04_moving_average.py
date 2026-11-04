from collections import deque

META = {
    "title": "Moving average",
    "function": "moving_average",
    "prompt": (
        "Renvoie la moyenne de chaque fenêtre de `k` valeurs consécutives de "
        "`values`, de gauche à droite (liste vide s'il y a moins de `k` valeurs). "
        "Lève une `ValueError` si `k` n'est pas strictement positif. "
        "Jusqu'à 100 000 valeurs, avec de grandes fenêtres."
    ),
    "hints": [
        "Recalculer la somme de chaque fenêtre coûte `k` opérations par pas.",
        "D'une fenêtre à la suivante, une valeur entre et une valeur sort.",
        "Une `deque` retire en O(1) par la gauche (`popleft`).",
    ],
}


def moving_average(values: list[float], k: int) -> list[float]:
    """Reference solution."""
    if k <= 0:
        raise ValueError("k must be positive")
    window: deque[float] = deque()
    total = 0.0
    averages = []
    for value in values:
        window.append(value)
        total += value
        if len(window) > k:
            total -= window.popleft()
        if len(window) == k:
            averages.append(total / k)
    return averages


_N, _K = 100_000, 20_000

TEST_CASES = [
    {"args": ([1, 2, 3, 4, 5], 2), "expected": [1.5, 2.5, 3.5, 4.5], "compare": "approx"},
    {"args": ([4, 8, 6], 3), "expected": [6.0], "compare": "approx", "note": "une seule fenêtre"},
    {"args": ([1, 2], 3), "expected": [], "note": "moins de k valeurs"},
    {"args": ([1, 2], 0), "raises": ValueError, "note": "k nul"},
    {"args": (list(range(_N)), _K),
     "expected": [i + (_K - 1) / 2 for i in range(_N - _K + 1)],
     "compare": "approx", "note": "100 000 valeurs, fenêtre de 20 000 (performance)"},
]
