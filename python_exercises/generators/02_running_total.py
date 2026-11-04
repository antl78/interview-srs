META = {
    "title": "Lazy running total",
    "function": "running_total",
    "prompt": (
        "Renvoie un itérateur paresseux des sommes cumulées de `numbers` : "
        "pour `[1, 2, 3]`, il produit 1, 3, 6. `numbers` peut être infini : "
        "chaque somme doit être produite dès que sa valeur est lue."
    ),
    "hints": [
        "Construire une liste oblige à lire toute l'entrée avant de rendre quoi que ce soit.",
        "Une boucle `for` sur `numbers` avec un `yield` à chaque tour.",
        "`itertools.accumulate` fait exactement ça.",
    ],
}


def running_total(numbers):
    """Reference solution."""
    total = 0
    for n in numbers:
        total += n
        yield total


class Endless:
    """Entrée infinie : 1, 2, 3, …"""

    def __iter__(self):
        n = 1
        while True:
            yield n
            n += 1

    def __repr__(self):
        return "Endless(1, 2, 3, …)"


def require_iterator(result):
    if iter(result) is not result:
        raise TypeError(f"running_total() doit renvoyer un itérateur, pas un {type(result).__name__}")


def to_list(result, *args):
    require_iterator(result)
    return list(result)


def take_5(result, *args):
    require_iterator(result)
    return [next(result) for _ in range(5)]


TEST_CASES = [
    {"args": ([1, 2, 3, 4],), "then": to_list, "expected": [1, 3, 6, 10]},
    {"args": ([5, -5, 3],), "then": to_list, "expected": [5, 0, 3], "note": "valeurs négatives"},
    {"args": ([],), "then": to_list, "expected": [], "note": "entrée vide"},
    {
        "args": (Endless(),),
        "then": take_5,
        "expected": [1, 3, 6, 10, 15],
        "note": "entrée infinie : calcul paresseux obligatoire",
    },
]
