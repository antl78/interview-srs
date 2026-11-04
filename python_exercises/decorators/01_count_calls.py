META = {
    "title": "Count calls decorator",
    "function": "count_calls",
    "prompt": (
        "Écris un décorateur qui compte les appels de `func` dans un "
        "attribut `calls` de la fonction décorée (0 avant tout appel). La "
        "fonction décorée accepte les mêmes arguments que `func`, renvoie "
        "le même résultat et garde son nom et sa docstring."
    ),
    "hints": [
        "Le wrapper accepte n'importe quels arguments : `*args, **kwargs`.",
        "Une fonction est un objet : `wrapper.calls = 0` lui ajoute un attribut.",
        "`@functools.wraps(func)` recopie `__name__` et `__doc__` sur le wrapper.",
    ],
}

import functools


def count_calls(func):
    """Reference solution."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def square(x):
    """Return x squared."""
    return x * x


def power(base, exp=2):
    """Return base ** exp."""
    return base**exp


def call_square_twice(wrapped, func):
    results = [wrapped(2), wrapped(3)]
    return results, wrapped.calls


def calls_before_any_call(wrapped, func):
    return wrapped.calls


def name_and_doc(wrapped, func):
    return wrapped.__name__, wrapped.__doc__


def call_power_with_kwargs(wrapped, func):
    return wrapped(2, exp=3), wrapped.calls


TEST_CASES = [
    {"args": (square,), "then": call_square_twice, "expected": ([4, 9], 2)},
    {"args": (square,), "then": calls_before_any_call, "expected": 0, "note": "aucun appel"},
    {"args": (power,), "then": call_power_with_kwargs, "expected": (8, 1), "note": "arguments nommés transmis"},
    {
        "args": (square,),
        "then": name_and_doc,
        "expected": ("square", "Return x squared."),
        "note": "nom et docstring conservés",
    },
]
