META = {
    "title": "Build query string",
    "function": "build_query_string",
    "prompt": (
        "Construit une query string à partir des arguments nommés `params` : "
        "paires `clé=valeur` jointes par `&`, triées par clé. Les paramètres "
        "valant `None` sont ignorés ; `0`, `False` et `\"\"` sont conservés."
    ),
    "hints": [
        "`params` est un dict : `sorted(params.items())` trie par clé.",
        "`if value` écarte aussi 0, False et \"\" : teste `is not None`.",
    ],
}


def build_query_string(**params: object) -> str:
    """Reference solution."""
    return "&".join(
        f"{key}={value}" for key, value in sorted(params.items()) if value is not None
    )


TEST_CASES = [
    {"args": (), "kwargs": {"page": 2, "q": "duckdb"}, "expected": "page=2&q=duckdb"},
    {"args": (), "kwargs": {"b": 1, "a": 2}, "expected": "a=2&b=1", "note": "tri par clé"},
    {"args": (), "kwargs": {"q": "sql", "lang": None}, "expected": "q=sql", "note": "None ignoré"},
    {"args": (), "kwargs": {"offset": 0, "debug": False, "tag": ""},
     "expected": "debug=False&offset=0&tag=", "note": "0, False et \"\" conservés"},
    {"args": (), "expected": "", "note": "aucun paramètre"},
]
