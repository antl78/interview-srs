META = {
    "title": "Fibonacci generator",
    "function": "fibonacci",
    "prompt": (
        "Écris un générateur infini qui produit la suite de Fibonacci : "
        "0, 1, 1, 2, 3, 5, 8… L'appel `fibonacci()` doit renvoyer un "
        "générateur, sans rien calculer à l'avance."
    ),
    "hints": [
        "Une boucle `while True` ne bloque pas un générateur : chaque `yield` rend la main.",
        "Deux variables suffisent : `a, b = b, a + b`.",
    ],
}


def fibonacci():
    """Reference solution."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def require_generator(gen):
    import inspect

    if not inspect.isgenerator(gen):
        raise TypeError(f"fibonacci() doit renvoyer un générateur, pas un {type(gen).__name__}")


def take_10(gen):
    require_generator(gen)
    return [next(gen) for _ in range(10)]


def take_1(gen):
    require_generator(gen)
    return [next(gen)]


def terms_20_to_24(gen):
    from itertools import islice

    require_generator(gen)
    return list(islice(gen, 20, 25))


def term_100(gen):
    from itertools import islice

    require_generator(gen)
    return next(islice(gen, 100, None))


TEST_CASES = [
    {"args": (), "then": take_10, "expected": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]},
    {"args": (), "then": terms_20_to_24, "expected": [6765, 10946, 17711, 28657, 46368]},
    {"args": (), "then": take_1, "expected": [0], "note": "le premier terme est 0"},
    {
        "args": (),
        "then": term_100,
        "expected": 354224848179261915075,
        "note": "100e terme : suite infinie, pas de borne fixée à l'avance",
    },
]
