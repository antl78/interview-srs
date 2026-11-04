import heapq

META = {
    "title": "Kth largest",
    "function": "kth_largest",
    "prompt": (
        "Renvoie la `k`-ième plus grande valeur de `numbers` (`k = 1` : le "
        "maximum), les doublons comptant chacun. Lève une `ValueError` si `k` "
        "n'est pas entre 1 et `len(numbers)`."
    ),
    "hints": [
        "Les doublons comptent : pas de `set`.",
        "Trier tout marche, mais seuls les `k` plus grands t'intéressent.",
        "`heapq.nlargest(k, numbers)` ; attention, un indice négatif ne lève pas d'erreur.",
    ],
}


def kth_largest(numbers: list[int], k: int) -> int:
    """Reference solution."""
    if not 1 <= k <= len(numbers):
        raise ValueError("k out of range")
    return heapq.nlargest(k, numbers)[-1]


TEST_CASES = [
    {"args": ([3, 2, 1, 5, 6, 4], 2), "expected": 5},
    {"args": ([5, 5, 4], 2), "expected": 5, "note": "les doublons comptent"},
    {"args": ([-1, -5, -3], 1), "expected": -1, "note": "négatifs"},
    {"args": ([7], 1), "expected": 7, "note": "un seul élément"},
    {"args": ([1, 2], 3), "raises": ValueError, "note": "k trop grand"},
    {"args": ([1, 2], 0), "raises": ValueError, "note": "k nul"},
]
