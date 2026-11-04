META = {
    "title": "Group by length",
    "function": "group_by_length",
    "prompt": (
        "Regroupe les mots de `words` par longueur : renvoie un dictionnaire "
        "`longueur → liste des mots`. Chaque liste garde l'ordre d'apparition "
        "et les doublons."
    ),
    "hints": [
        "Il faut créer la liste la première fois qu'une longueur apparaît.",
        "`d.setdefault(clé, []).append(x)` fait les deux en une ligne.",
    ],
}


def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Reference solution."""
    groups: dict[int, list[str]] = {}
    for word in words:
        groups.setdefault(len(word), []).append(word)
    return groups


TEST_CASES = [
    {"args": (["a", "bb", "c", "dd", "eee"],), "expected": {1: ["a", "c"], 2: ["bb", "dd"], 3: ["eee"]}},
    {"args": (["sql", "py", "duck", "db"],), "expected": {3: ["sql"], 2: ["py", "db"], 4: ["duck"]}},
    {"args": (["hi", "hi"],), "expected": {2: ["hi", "hi"]}, "note": "doublons conservés"},
    {"args": (["b", "a"],), "expected": {1: ["b", "a"]}, "note": "ordre d'apparition, pas de tri"},
    {"args": ([""],), "expected": {0: [""]}, "note": "mot vide"},
    {"args": ([],), "expected": {}, "note": "liste vide"},
]
