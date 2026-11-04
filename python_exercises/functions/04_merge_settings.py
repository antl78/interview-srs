META = {
    "title": "Merge settings",
    "function": "merge_settings",
    "prompt": (
        "Renvoie un nouveau dictionnaire : `defaults` mis à jour par les "
        "arguments nommés `overrides`. Lève une `ValueError` si une clé de "
        "`overrides` n'existe pas dans `defaults`. `None`, `0` et `False` sont "
        "de vraies valeurs : elles remplacent la valeur par défaut."
    ),
    "hints": [
        "`overrides.keys() - defaults.keys()` donne les clés inconnues.",
        "`{**a, **b}` fusionne deux dicts, `b` l'emportant.",
    ],
}


def merge_settings(defaults: dict, **overrides: object) -> dict:
    """Reference solution."""
    unknown = overrides.keys() - defaults.keys()
    if unknown:
        raise ValueError(f"unknown settings: {sorted(unknown)}")
    return {**defaults, **overrides}


TEST_CASES = [
    {"args": ({"theme": "light", "size": 12},), "kwargs": {"size": 14},
     "expected": {"theme": "light", "size": 14}},
    {"args": ({"a": 1, "b": 2},), "kwargs": {"a": 10, "b": 20}, "expected": {"a": 10, "b": 20}},
    {"args": ({"a": 1},), "expected": {"a": 1}, "note": "aucun override"},
    {"args": ({"debug": True, "retries": 3, "proxy": "x"},),
     "kwargs": {"debug": False, "retries": 0, "proxy": None},
     "expected": {"debug": False, "retries": 0, "proxy": None},
     "note": "False, 0 et None remplacent"},
    {"args": ({"a": 1},), "kwargs": {"b": 2}, "raises": ValueError, "note": "clé inconnue"},
]
