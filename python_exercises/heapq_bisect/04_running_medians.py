import heapq

META = {
    "title": "Running medians",
    "function": "running_medians",
    "prompt": (
        "Renvoie, après l'ajout de chaque valeur de `values`, la médiane des "
        "valeurs reçues jusque-là (moyenne des deux valeurs centrales si leur "
        "nombre est pair). Jusqu'à 100 000 valeurs."
    ),
    "hints": [
        "Retrier à chaque ajout est trop lent.",
        "Sépare les valeurs en deux moitiés : il suffit de connaître le maximum de l'une et le minimum de l'autre.",
        "Deux tas : `heapq` est un min-heap, stocke les opposés (`-x`) pour la moitié basse.",
    ],
}


def running_medians(values: list[int]) -> list[float]:
    """Reference solution."""
    low: list[int] = []   # moitié basse, valeurs opposées (max-heap)
    high: list[int] = []  # moitié haute (min-heap), autant ou une de plus que low
    medians = []
    for value in values:
        heapq.heappush(low, -heapq.heappushpop(high, value))
        if len(low) > len(high):
            heapq.heappush(high, -heapq.heappop(low))
        if len(high) > len(low):
            medians.append(float(high[0]))
        else:
            medians.append((high[0] - low[0]) / 2)
    return medians


_N = 100_000

TEST_CASES = [
    {"args": ([2, 1, 5, 7, 2, 0, 5],), "expected": [2, 1.5, 2, 3.5, 2, 2, 2], "compare": "approx"},
    {"args": ([-3, -1],), "expected": [-3, -2], "compare": "approx", "note": "négatifs"},
    {"args": ([3, 3, 3],), "expected": [3, 3, 3], "compare": "approx", "note": "doublons"},
    {"args": ([4],), "expected": [4], "compare": "approx", "note": "une seule valeur"},
    {"args": ([],), "expected": [], "note": "liste vide"},
    {"args": (list(range(_N - 1, -1, -1)),),
     "expected": [(2 * _N - 2 - i) / 2 for i in range(_N)],
     "compare": "approx", "note": "100 000 valeurs (performance)"},
]
