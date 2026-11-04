META = {
    "title": "Multiplier functions",
    "function": "make_multipliers",
    "prompt": (
        "Renvoie une liste de `n` fonctions : la fonction d'indice `i` "
        "multiplie son argument par `i`. Ainsi `make_multipliers(3)[2](10)` "
        "vaut 20."
    ),
    "hints": [
        "Teste `[f(10) for f in make_multipliers(3)]` : obtiens-tu bien `[0, 10, 20]` ?",
        "Une closure capture la variable, pas sa valeur au moment de la création (late binding).",
        "Fige la valeur avec un argument par défaut (`lambda x, i=i: x * i`) ou une fonction usine.",
    ],
}


def make_multipliers(n: int) -> list:
    """Reference solution."""
    return [lambda x, i=i: x * i for i in range(n)]


def require_list(functions):
    if type(functions) is not list:
        raise TypeError(f"make_multipliers() doit renvoyer une liste, pas un {type(functions).__name__}")


def apply_to_10(functions, *args):
    require_list(functions)
    return [f(10) for f in functions]


def apply_to_minus_2(functions, *args):
    require_list(functions)
    return [f(-2) for f in functions]


TEST_CASES = [
    {"args": (4,), "then": apply_to_10, "expected": [0, 10, 20, 30]},
    {"args": (3,), "then": apply_to_minus_2, "expected": [0, -2, -4]},
    {"args": (1,), "then": apply_to_10, "expected": [0], "note": "une seule fonction"},
    {"args": (0,), "then": apply_to_10, "expected": [], "note": "aucune fonction"},
]
