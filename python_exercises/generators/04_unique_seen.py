META = {
    "title": "Lazy unique elements",
    "function": "unique_seen",
    "prompt": (
        "Renvoie un itérateur paresseux des éléments de `iterable` sans "
        "doublons, dans l'ordre de leur première apparition. `iterable` peut "
        "être infini : un élément doit être produit dès qu'il est rencontré."
    ),
    "hints": [
        "`set(iterable)` lit toute l'entrée et perd l'ordre.",
        "Garde les éléments déjà vus dans un `set`, et produis les autres au fil de l'eau.",
    ],
}


def unique_seen(iterable):
    """Reference solution."""
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item


class Cycle:
    """Entrée infinie qui répète `items` en boucle."""

    def __init__(self, items):
        self.items = list(items)

    def __iter__(self):
        while True:
            yield from self.items

    def __repr__(self):
        return f"Cycle({self.items!r})"


def require_iterator(result):
    if iter(result) is not result:
        raise TypeError(f"unique_seen() doit renvoyer un itérateur, pas un {type(result).__name__}")


def to_list(result, *args):
    require_iterator(result)
    return list(result)


def take_3(result, *args):
    require_iterator(result)
    return [next(result) for _ in range(3)]


TEST_CASES = [
    {"args": ([3, 1, 3, 2, 1],), "then": to_list, "expected": [3, 1, 2]},
    {"args": ("abracadabra",), "then": to_list, "expected": ["a", "b", "r", "c", "d"], "note": "une chaîne est itérable"},
    {"args": ([],), "then": to_list, "expected": [], "note": "entrée vide"},
    {
        "args": (Cycle([1, 2, 1, 3]),),
        "then": take_3,
        "expected": [1, 2, 3],
        "note": "entrée infinie : ordre d'apparition, sans tout lire",
    },
]
