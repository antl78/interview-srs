META = {
    "title": "Join parts",
    "function": "join_parts",
    "prompt": (
        "Renvoie tous les arguments positionnels `parts`, convertis en `str`, "
        "joints par `sep` (par défaut `\"-\"`). `sep` ne peut être passé que "
        "par son nom."
    ),
    "hints": [
        "Un paramètre placé après `*parts` est forcément nommé (keyword-only).",
        "`str.join` n'accepte que des chaînes : convertis avec `str()`.",
    ],
}


def join_parts(*parts: object, sep: str = "-") -> str:
    """Reference solution."""
    return sep.join(str(part) for part in parts)


TEST_CASES = [
    {"args": ("a", "b", "c"), "expected": "a-b-c"},
    {"args": ("2026", "11", "04"), "kwargs": {"sep": "/"}, "expected": "2026/11/04"},
    {"args": (1, 2.5, None), "expected": "1-2.5-None", "note": "conversion en str"},
    {"args": ("solo",), "kwargs": {"sep": ", "}, "expected": "solo", "note": "une seule partie"},
    {"args": (), "expected": "", "note": "aucun argument"},
]
