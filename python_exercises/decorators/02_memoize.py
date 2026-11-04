META = {
    "title": "Memoize decorator",
    "function": "memoize",
    "prompt": (
        "Écris un décorateur qui met en cache les résultats de `func` : un "
        "appel avec des arguments déjà vus (positionnels et nommés) renvoie "
        "le résultat mémorisé sans rappeler `func`. Les arguments sont "
        "hashables. Sans `functools.cache` ni `lru_cache`."
    ),
    "hints": [
        "Un `dict` dans la closure, indexé par les arguments.",
        "La clé doit contenir les `kwargs` aussi : `(args, tuple(sorted(kwargs.items())))`.",
        "Un résultat peut valoir `None` ou 0 : teste `key in cache`, pas `cache.get(key)`.",
    ],
}

import functools


def memoize(func):
    """Reference solution."""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


class Spy:
    """Fonction espionne : compte ses appels dans `calls`."""

    def __init__(self, name, body):
        self.name = name
        self.body = body
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.body(*args, **kwargs)

    def __repr__(self):
        return self.name


def square_body(x):
    return x * x


def power_body(base, exp=2):
    return base**exp


def nothing_body(x):
    return None


def same_arg_twice(wrapped, spy):
    return [wrapped(3), wrapped(3)], spy.calls


def mixed_args(wrapped, spy):
    return [wrapped(3), wrapped(4), wrapped(3), wrapped(4)], spy.calls


def kwargs_in_key(wrapped, spy):
    return [wrapped(2), wrapped(2, exp=3), wrapped(2, exp=3)], spy.calls


def none_result_twice(wrapped, spy):
    return [wrapped(1), wrapped(1)], spy.calls


TEST_CASES = [
    {"args": (Spy("square", square_body),), "then": same_arg_twice, "expected": ([9, 9], 1)},
    {"args": (Spy("square", square_body),), "then": mixed_args, "expected": ([9, 16, 9, 16], 2)},
    {
        "args": (Spy("power", power_body),),
        "then": kwargs_in_key,
        "expected": ([4, 8, 8], 2),
        "note": "les arguments nommés font partie de la clé",
    },
    {
        "args": (Spy("nothing", nothing_body),),
        "then": none_result_twice,
        "expected": ([None, None], 1),
        "note": "un résultat None est mis en cache aussi",
    },
]
