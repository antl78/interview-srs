META = {
    "title": "Atomic list update",
    "function": "atomic_update",
    "prompt": (
        "Renvoie un context manager qui donne (`as`) une copie de travail "
        "de `items`, indépendante même pour les listes imbriquées. Si le "
        "bloc se termine normalement, `items` prend, sur place, le contenu "
        "de la copie. Si le bloc lève une exception, `items` reste intact "
        "et l'exception remonte."
    ),
    "hints": [
        "`yield draft` : c'est la valeur reçue par `as`.",
        "Le code après le `yield` ne s'exécute que si le bloc n'a pas levé d'exception.",
        "`copy.deepcopy` pour la copie, `items[:] = draft` pour modifier sur place.",
    ],
}

import contextlib
import copy


@contextlib.contextmanager
def atomic_update(items: list):
    """Reference solution."""
    draft = copy.deepcopy(items)
    yield draft
    items[:] = draft


def append_4_remove_1(cm, items):
    with cm as draft:
        draft.append(4)
        draft.remove(1)
    return items


def failure_midway(cm, items):
    try:
        with cm as draft:
            draft.append(4)
            raise ValueError("invalid")
    except ValueError:
        pass
    return items


def failure_on_nested(cm, items):
    try:
        with cm as draft:
            draft[0].append(99)
            raise ValueError("invalid")
    except ValueError:
        pass
    return items


def error_in_block(cm, items):
    with cm:
        raise ValueError("invalid")


TEST_CASES = [
    {"args": ([1, 2, 3],), "then": append_4_remove_1, "expected": [2, 3, 4]},
    {"args": ([1, 2, 3],), "then": failure_midway, "expected": [1, 2, 3], "note": "exception : rien n'est modifié"},
    {"args": ([[1], [2]],), "then": failure_on_nested, "expected": [[1], [2]], "note": "listes imbriquées : copie profonde"},
    {"args": ([1, 2, 3],), "then": error_in_block, "raises": ValueError, "note": "l'exception remonte"},
]
