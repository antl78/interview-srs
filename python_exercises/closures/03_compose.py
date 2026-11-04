META = {
    "title": "Compose functions",
    "function": "compose",
    "prompt": (
        "Renvoie la composée de `functions`, appliquées de droite à gauche : "
        "`compose(f, g)(x)` vaut `f(g(x))`. Sans fonction, la composée "
        "renvoie son argument tel quel."
    ),
    "hints": [
        "La fonction renvoyée parcourt `functions` à chaque appel.",
        "La dernière fonction de la liste s'applique en premier : `reversed(functions)`.",
    ],
}


def compose(*functions):
    """Reference solution."""

    def composed(x):
        for f in reversed(functions):
            x = f(x)
        return x

    return composed


def add_one(x):
    return x + 1


def double(x):
    return 2 * x


def square(x):
    return x * x


def apply_to_3(composed, *functions):
    return composed(3)


TEST_CASES = [
    {"args": (add_one, double), "then": apply_to_3, "expected": 7},
    {"args": (add_one, square, double), "then": apply_to_3, "expected": 37},
    {"args": (double, add_one), "then": apply_to_3, "expected": 8, "note": "ordre : la dernière s'applique en premier"},
    {"args": (square,), "then": apply_to_3, "expected": 9, "note": "une seule fonction"},
    {"args": (), "then": apply_to_3, "expected": 3, "note": "aucune fonction : identité"},
]
