from functools import cmp_to_key

META = {
    "title": "Largest number",
    "function": "largest_number",
    "prompt": (
        "Concatène les entiers positifs ou nuls de `numbers` (liste non vide) "
        "dans l'ordre qui forme le plus grand nombre possible, et renvoie-le "
        "sous forme de chaîne, sans zéro inutile en tête."
    ),
    "hints": [
        "Trier les chaînes par ordre décroissant ne suffit pas : essaie `[3, 30]`.",
        "`a` doit passer avant `b` si `a + b > b + a` (en chaînes).",
        "`functools.cmp_to_key` transforme une fonction de comparaison en clé de tri.",
    ],
}


def largest_number(numbers: list[int]) -> str:
    """Reference solution."""

    def compare(a: str, b: str) -> int:
        # Négatif : a passe avant b.
        return (a + b < b + a) - (a + b > b + a)

    digits = sorted(map(str, numbers), key=cmp_to_key(compare))
    return "".join(digits).lstrip("0") or "0"


TEST_CASES = [
    {"args": ([10, 2],), "expected": "210"},
    {"args": ([3, 30, 34, 5, 9],), "expected": "9534330", "note": "un tri de chaînes ne suffit pas"},
    {"args": ([121, 12],), "expected": "12121", "note": "préfixe commun"},
    {"args": ([824, 8247],), "expected": "8248247", "note": "préfixe commun"},
    {"args": ([0, 0],), "expected": "0", "note": "que des zéros"},
    {"args": ([1],), "expected": "1", "note": "un seul nombre"},
]
