META = {
    "title": "Unique records",
    "function": "unique_records",
    "prompt": (
        "Supprime les doublons de `records` (liste de dicts aux valeurs "
        "hashables) en gardant la première occurrence, dans l'ordre d'origine. "
        "Deux dicts sont des doublons s'ils ont les mêmes clés et valeurs, quel "
        "que soit l'ordre des clés. Jusqu'à 40 000 dicts."
    ),
    "hints": [
        "`record not in unique` reparcourt la liste à chaque fois.",
        "Un `dict` n'est pas hashable : il ne peut pas aller dans un `set`.",
        "`frozenset(record.items())` est hashable et ignore l'ordre des clés.",
    ],
}


def unique_records(records: list[dict]) -> list[dict]:
    """Reference solution."""
    seen: set[frozenset] = set()
    unique = []
    for record in records:
        key = frozenset(record.items())
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique


TEST_CASES = [
    {"args": ([{"id": 1}, {"id": 2}, {"id": 1}],), "expected": [{"id": 1}, {"id": 2}]},
    {"args": ([{"a": 1, "b": 2}, {"b": 2, "a": 1}],), "expected": [{"a": 1, "b": 2}],
     "note": "ordre des clés différent"},
    {"args": ([{"a": 1}, {"a": 1, "b": None}],), "expected": [{"a": 1}, {"a": 1, "b": None}],
     "note": "une clé en plus"},
    {"args": ([],), "expected": [], "note": "liste vide"},
    {"args": ([{"id": i % 20_000} for i in range(40_000)],),
     "expected": [{"id": i} for i in range(20_000)], "note": "40 000 dicts (performance)"},
]
