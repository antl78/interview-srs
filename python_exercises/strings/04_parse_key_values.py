META = {
    "title": "Parse key values",
    "function": "parse_key_values",
    "prompt": (
        "`text` contient des paires `clé=valeur` séparées par des `;`. Renvoie "
        "le dictionnaire correspondant (clés et valeurs en `str`, sans les "
        "espaces autour). Les segments vides sont ignorés ; une valeur peut "
        "contenir `=`."
    ),
    "hints": [
        "Découpe d'abord sur `;`, puis chaque segment sur `=`.",
        "`split(\"=\", 1)` ne coupe qu'au premier `=` ; `strip()` retire les espaces.",
    ],
}


def parse_key_values(text: str) -> dict[str, str]:
    """Reference solution."""
    result = {}
    for part in text.split(";"):
        if not part.strip():
            continue
        key, value = part.split("=", 1)
        result[key.strip()] = value.strip()
    return result


TEST_CASES = [
    {"args": ("a=1;b=2",), "expected": {"a": "1", "b": "2"}},
    {"args": (" host = localhost ; port=8080 ",),
     "expected": {"host": "localhost", "port": "8080"}, "note": "espaces autour"},
    {"args": ("token=abc==;user=bob",), "expected": {"token": "abc==", "user": "bob"},
     "note": "valeur contenant ="},
    {"args": ("a=1;; b=2;",), "expected": {"a": "1", "b": "2"}, "note": "segments vides"},
    {"args": ("",), "expected": {}, "note": "chaîne vide"},
]
