from itertools import islice

META = {
    "title": "Chunked",
    "function": "chunked",
    "prompt": (
        "Découpe `items` en listes de `size` éléments consécutifs ; le dernier "
        "paquet peut être plus court. Lève une `ValueError` si `size` n'est pas "
        "strictement positif."
    ),
    "hints": [
        "Attention au dernier paquet incomplet, et à ne pas en créer un vide.",
        "Le découpage par tranches `items[i:i + size]` marche ; `range` a un pas.",
        "Version itérateur : `islice(iterator, size)` prend les `size` éléments suivants.",
    ],
}


def chunked(items: list[int], size: int) -> list[list[int]]:
    """Reference solution."""
    if size <= 0:
        raise ValueError("size must be positive")
    iterator = iter(items)
    chunks = []
    while chunk := list(islice(iterator, size)):
        chunks.append(chunk)
    return chunks


TEST_CASES = [
    {"args": ([1, 2, 3, 4, 5], 2), "expected": [[1, 2], [3, 4], [5]],
     "note": "dernier paquet incomplet"},
    {"args": ([1, 2, 3, 4], 2), "expected": [[1, 2], [3, 4]], "note": "pas de paquet vide à la fin"},
    {"args": ([1, 2], 5), "expected": [[1, 2]], "note": "size plus grand que la liste"},
    {"args": ([], 3), "expected": [], "note": "liste vide"},
    {"args": ([1], 0), "raises": ValueError, "note": "size nul"},
]
