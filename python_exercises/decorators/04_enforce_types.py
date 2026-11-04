META = {
    "title": "Enforce types decorator",
    "function": "enforce_types",
    "prompt": (
        "Écris un décorateur qui vérifie, à chaque appel, que les arguments "
        "passés (positionnels ou nommés) sont des instances (`isinstance`) "
        "de la classe annotée sur leur paramètre, et lève une `TypeError` "
        "sinon. Les paramètres sans annotation et les valeurs par défaut ne "
        "sont pas vérifiés ; l'annotation de retour est ignorée."
    ),
    "hints": [
        "`inspect.signature(func).bind(*args, **kwargs)` associe chaque argument à son paramètre.",
        "`bound.arguments` ne contient que les arguments réellement passés.",
        "`func.__annotations__` contient aussi la clé `'return'`.",
    ],
}

import functools
import inspect


def enforce_types(func):
    """Reference solution."""
    signature = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            expected = signature.parameters[name].annotation
            if expected is not inspect.Parameter.empty and not isinstance(value, expected):
                raise TypeError(f"{name} must be {expected.__name__}")
        return func(*args, **kwargs)

    return wrapper


def label(name: str, count: int = 1, extra=None) -> str:
    return f"{name} x{count}"


def call_ok(wrapped, func):
    return wrapped("tea", 3)


def call_with_default(wrapped, func):
    return wrapped("tea")


def call_count_as_str_kwarg(wrapped, func):
    return wrapped("tea", count="3")


def call_name_as_int(wrapped, func):
    return wrapped(42)


def call_with_unannotated_extra(wrapped, func):
    return wrapped("tea", 2, extra=[1, 2])


TEST_CASES = [
    {"args": (label,), "then": call_ok, "expected": "tea x3"},
    {"args": (label,), "then": call_name_as_int, "raises": TypeError},
    {"args": (label,), "then": call_count_as_str_kwarg, "raises": TypeError, "note": "argument nommé vérifié aussi"},
    {"args": (label,), "then": call_with_default, "expected": "tea x1", "note": "valeur par défaut non vérifiée"},
    {"args": (label,), "then": call_with_unannotated_extra, "expected": "tea x2", "note": "paramètre sans annotation"},
]
