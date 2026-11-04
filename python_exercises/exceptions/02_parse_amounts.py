import math

META = {
    "title": "Parse amounts",
    "function": "parse_amounts",
    "prompt": (
        "Convertis chaque élément de `raw_values` en `float` et renvoie les "
        "valeurs valides, dans l'ordre. Les éléments qui ne représentent pas un "
        "nombre fini (texte, `None`, `\"nan\"`, `\"inf\"`) sont ignorés."
    ),
    "hints": [
        "Plutôt que de tester le format à la main, essaie de convertir et rattrape l'échec.",
        "`float(None)` ne lève pas la même exception que `float(\"abc\")`.",
        "`float(\"nan\")` réussit : `math.isfinite` fait le tri.",
    ],
}


def parse_amounts(raw_values: list[str | None]) -> list[float]:
    """Reference solution."""
    amounts = []
    for raw in raw_values:
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if math.isfinite(value):
            amounts.append(value)
    return amounts


TEST_CASES = [
    {"args": (["12.5", "abc", "-3", " 4 "],), "expected": [12.5, -3.0, 4.0],
     "note": "négatif et espaces"},
    {"args": (["1e3"],), "expected": [1000.0], "note": "notation scientifique"},
    {"args": ([None, "2"],), "expected": [2.0], "note": "None"},
    {"args": (["nan", "inf", "7"],), "expected": [7.0], "note": "valeurs non finies"},
    {"args": (["", " "],), "expected": [], "note": "chaînes vides"},
    {"args": ([],), "expected": [], "note": "liste vide"},
]
