META = {
    "title": "Suppress errors",
    "function": "suppress_errors",
    "prompt": (
        "Renvoie un context manager qui supprime les exceptions des types "
        "`exceptions` (sous-classes comprises) levées dans le bloc `with` : "
        "l'exécution reprend après le bloc. Les autres exceptions remontent. "
        "Sans `contextlib.suppress`, qui fait exactement ça."
    ),
    "hints": [
        "`@contextlib.contextmanager` transforme un générateur à un seul `yield` en context manager.",
        "Une exception levée dans le bloc `with` ressort au niveau du `yield`.",
        "`except exceptions:` accepte un tuple de classes.",
    ],
}

import contextlib


@contextlib.contextmanager
def suppress_errors(*exceptions):
    """Reference solution."""
    try:
        yield
    except exceptions:
        pass


def key_error_in_body(cm, *exceptions):
    log = []
    with cm:
        log.append("start")
        raise KeyError("missing")
    log.append("after")
    return log


def index_error_in_body(cm, *exceptions):
    log = []
    with cm:
        log.append("start")
        raise IndexError("out of range")
    log.append("after")
    return log


def value_error_in_body(cm, *exceptions):
    with cm:
        raise ValueError("not listed")
    return "after"


def no_error_in_body(cm, *exceptions):
    log = []
    with cm:
        log.append("start")
        log.append("end")
    log.append("after")
    return log


TEST_CASES = [
    {"args": (KeyError,), "then": key_error_in_body, "expected": ["start", "after"]},
    {"args": (KeyError, IndexError), "then": index_error_in_body, "expected": ["start", "after"], "note": "plusieurs types"},
    {"args": (LookupError,), "then": key_error_in_body, "expected": ["start", "after"], "note": "sous-classe : KeyError hérite de LookupError"},
    {"args": (KeyError,), "then": value_error_in_body, "raises": ValueError, "note": "exception non listée : elle remonte"},
    {"args": (KeyError,), "then": no_error_in_body, "expected": ["start", "end", "after"], "note": "bloc sans exception"},
]
