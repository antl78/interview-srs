META = {
    "title": "Count Vowels",
    "function": "count_vowels",
    "prompt": (
        "Renvoie le nombre de voyelles (`a`, `e`, `i`, `o`, `u`) dans `text`, "
        "en comptant aussi les majuscules."
    ),
    "hints": [
        "Une boucle `for` sur une chaîne parcourt ses caractères un par un.",
        "`char.lower() in \"aeiou\"` traite majuscules et minuscules d'un coup.",
    ],
}


def count_vowels(text: str) -> int:
    """Reference solution."""
    count = 0
    for char in text:
        if char.lower() in "aeiou":
            count += 1
    return count


TEST_CASES = [
    {"args": ("hello",), "expected": 2},
    {"args": ("python",), "expected": 1},
    {"args": ("AEIOU",), "expected": 5, "note": "majuscules"},
    {"args": ("rhythm",), "expected": 0, "note": "aucune voyelle"},
    {"args": ("",), "expected": 0, "note": "chaîne vide"},
]
