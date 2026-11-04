from collections import deque

META = {
    "title": "Interleave iterables",
    "function": "interleave",
    "prompt": (
        "Renvoie un itérateur paresseux qui alterne les éléments des "
        "`iterables` (un de chaque, à tour de rôle). Quand un itérable est "
        "épuisé, on continue avec les autres. Un itérable peut être infini."
    ),
    "hints": [
        "`zip` s'arrête au plus court : il perd la fin des plus longs.",
        "Garde une liste d'itérateurs encore actifs, et retire ceux qui lèvent `StopIteration`.",
        "Une `deque` d'itérateurs fait une bonne file : `popleft`, `next`, puis `append` s'il en reste.",
    ],
}


def interleave(*iterables):
    """Reference solution."""
    queue = deque(iter(it) for it in iterables)
    while queue:
        it = queue.popleft()
        try:
            yield next(it)
        except StopIteration:
            continue
        queue.append(it)


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
        raise TypeError(f"interleave() doit renvoyer un itérateur, pas un {type(result).__name__}")


def to_list(result, *args):
    require_iterator(result)
    return list(result)


def take_6(result, *args):
    require_iterator(result)
    return [next(result) for _ in range(6)]


TEST_CASES = [
    {"args": ([1, 2, 3], "ab"), "then": to_list, "expected": [1, "a", 2, "b", 3]},
    {"args": ([1], [2, 3, 4], [5, 6]), "then": to_list, "expected": [1, 2, 5, 3, 6, 4], "note": "longueurs différentes"},
    {"args": ([], [1, 2]), "then": to_list, "expected": [1, 2], "note": "un itérable vide"},
    {"args": (), "then": to_list, "expected": [], "note": "aucun itérable"},
    {
        "args": (Endless(), [10, 20]),
        "then": take_6,
        "expected": [1, 10, 2, 20, 3, 4],
        "note": "un itérable infini",
    },
]
