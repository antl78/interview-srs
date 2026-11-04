from collections import defaultdict

META = {
    "title": "Group anagrams",
    "function": "group_anagrams",
    "prompt": (
        "Regroupe les mots de `words` qui sont des anagrammes les uns des autres. "
        "Renvoie une liste de listes : les groupes dans l'ordre de leur première "
        "apparition, les mots dans leur ordre d'origine (doublons conservés)."
    ),
    "hints": [
        "Deux anagrammes ont une même « signature » : laquelle ?",
        "Les lettres triées forment une clé de dict ; `defaultdict(list)` évite de tester la clé.",
        "`dict.values()` n'est pas une liste.",
    ],
}


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Reference solution."""
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())


TEST_CASES = [
    {"args": (["eat", "tea", "tan", "ate", "nat", "bat"],),
     "expected": [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]},
    {"args": (["aab", "abb"],), "expected": [["aab"], ["abb"]],
     "note": "mêmes lettres, pas les mêmes comptes"},
    {"args": (["ab", "ba", "ab"],), "expected": [["ab", "ba", "ab"]], "note": "doublons conservés"},
    {"args": ([],), "expected": [], "note": "liste vide"},
    {"args": (["", ""],), "expected": [["", ""]], "note": "mots vides"},
]
