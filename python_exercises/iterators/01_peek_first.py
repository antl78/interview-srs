from itertools import chain

META = {
    "title": "Peek first element",
    "function": "peek_first",
    "prompt": (
        "Renvoie un tuple `(first, iterator)` : le premier élément de "
        "`iterable`, et un itérateur qui produit tous les éléments, premier "
        "compris. `iterable` peut n'être lisible qu'une seule fois, ou être "
        "infini. Lève une `ValueError` si `iterable` est vide."
    ),
    "hints": [
        "Pour lire le premier élément, il faut le consommer : il faut donc le remettre devant.",
        "`next(it)` lève `StopIteration` sur un itérateur vide.",
        "`itertools.chain([first], it)` recolle le premier élément au reste.",
    ],
}


def peek_first(iterable) -> tuple:
    """Reference solution."""
    it = iter(iterable)
    try:
        first = next(it)
    except StopIteration:
        raise ValueError("empty iterable") from None
    return first, chain([first], it)


class OnePass:
    """Itérable lisible une seule fois, comme un fichier ou un générateur."""

    def __init__(self, items):
        self.items = list(items)
        self.used = False

    def __iter__(self):
        if self.used:
            return iter(())
        self.used = True
        return iter(self.items)

    def __repr__(self):
        return f"OnePass({self.items!r})"


class Endless:
    """Entrée infinie : 1, 2, 3, …"""

    def __iter__(self):
        n = 1
        while True:
            yield n
            n += 1

    def __repr__(self):
        return "Endless(1, 2, 3, …)"


def first_and_all(result, *args):
    first, it = result
    return first, list(it)


def first_and_next_3(result, *args):
    first, it = result
    return first, [next(it) for _ in range(3)]


TEST_CASES = [
    {"args": ([1, 2, 3],), "then": first_and_all, "expected": (1, [1, 2, 3])},
    {"args": ("abc",), "then": first_and_all, "expected": ("a", ["a", "b", "c"])},
    {
        "args": (OnePass([4, 5, 6]),),
        "then": first_and_all,
        "expected": (4, [4, 5, 6]),
        "note": "itérable lisible une seule fois",
    },
    {
        "args": (Endless(),),
        "then": first_and_next_3,
        "expected": (1, [1, 2, 3]),
        "note": "entrée infinie : ne lire que le premier élément",
    },
    {"args": ([None, 0],), "then": first_and_all, "expected": (None, [None, 0]), "note": "premier élément None"},
    {"args": (OnePass([]),), "then": first_and_all, "raises": ValueError, "note": "itérable vide"},
]
