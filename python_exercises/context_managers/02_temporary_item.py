META = {
    "title": "Temporary dict item",
    "function": "temporary_item",
    "prompt": (
        "Renvoie un context manager qui, dans le bloc `with`, fixe "
        "`mapping[key] = value`, puis remet `mapping` dans son état "
        "d'origine à la sortie, même si le bloc lève une exception (qui "
        "remonte) : ancienne valeur restaurée, ou clé supprimée si elle "
        "n'existait pas."
    ),
    "hints": [
        "Sauvegarde l'état avant de modifier : la clé existait-elle, et avec quelle valeur ?",
        "`try` / `finally` autour du `yield` garantit la restauration.",
        "Une ancienne valeur peut être `None` : `key in mapping`, pas `mapping.get(key)`.",
    ],
}

import contextlib


@contextlib.contextmanager
def temporary_item(mapping: dict, key, value):
    """Reference solution."""
    existed = key in mapping
    old = mapping.get(key)
    mapping[key] = value
    try:
        yield
    finally:
        if existed:
            mapping[key] = old
        else:
            del mapping[key]


def inside_and_after(cm, mapping, key, value):
    with cm:
        inside = dict(mapping)
    return inside, mapping


def after_error(cm, mapping, key, value):
    try:
        with cm:
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    return mapping


def error_in_block(cm, mapping, key, value):
    with cm:
        raise RuntimeError("boom")


TEST_CASES = [
    {"args": ({"a": 1}, "a", 2), "then": inside_and_after, "expected": ({"a": 2}, {"a": 1})},
    {"args": ({"a": 1}, "b", 2), "then": inside_and_after, "expected": ({"a": 1, "b": 2}, {"a": 1}), "note": "clé absente : supprimée à la sortie"},
    {"args": ({"a": None}, "a", 5), "then": inside_and_after, "expected": ({"a": 5}, {"a": None}), "note": "ancienne valeur None"},
    {"args": ({"a": 1}, "a", 2), "then": after_error, "expected": {"a": 1}, "note": "restauré après une exception"},
    {"args": ({}, "a", 2), "then": after_error, "expected": {}, "note": "clé absente, puis exception"},
    {"args": ({"a": 1}, "a", 2), "then": error_in_block, "raises": RuntimeError, "note": "l'exception n'est pas avalée"},
]
