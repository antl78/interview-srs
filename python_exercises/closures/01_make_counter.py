META = {
    "title": "Counter factory",
    "function": "make_counter",
    "prompt": (
        "Renvoie une fonction sans argument qui, à chaque appel, renvoie la "
        "valeur suivante d'un compteur : `start` au premier appel, puis "
        "`start + step`, `start + 2 * step`… Pas de variable globale."
    ),
    "hints": [
        "La fonction renvoyée garde accès aux variables de `make_counter` : c'est une closure.",
        "Réaffecter une variable capturée exige `nonlocal`, sinon `UnboundLocalError`.",
    ],
}


def make_counter(start: int = 0, step: int = 1):
    """Reference solution."""
    current = start - step

    def counter() -> int:
        nonlocal current
        current += step
        return current

    return counter


def call_3_times(counter, *args, **kwargs):
    return [counter(), counter(), counter()]


TEST_CASES = [
    {"args": (), "then": call_3_times, "expected": [0, 1, 2]},
    {"args": (10,), "then": call_3_times, "expected": [10, 11, 12]},
    {"args": (), "kwargs": {"step": -5}, "then": call_3_times, "expected": [0, -5, -10], "note": "pas négatif"},
    {"args": (7, 0), "then": call_3_times, "expected": [7, 7, 7], "note": "pas nul"},
]
