META = {
    "title": "Retry decorator factory",
    "function": "retry",
    "prompt": (
        "Écris une decorator factory : `@retry(times)` rappelle la fonction "
        "décorée tant qu'elle lève une exception, avec au plus `times` essais "
        "au total. Si tous échouent, la dernière exception remonte. Lève une "
        "`ValueError` dès l'appel `retry(times)` si `times` vaut moins de 1."
    ),
    "hints": [
        "Trois niveaux de fonctions : `retry(times)` renvoie un décorateur, qui renvoie le wrapper.",
        "Une boucle `for attempt in range(times)` avec un `try` dedans.",
        "Au dernier essai, laisse l'exception remonter (`raise` seul dans le `except`).",
    ],
}

import functools


def retry(times: int):
    """Reference solution."""
    if times < 1:
        raise ValueError("times must be at least 1")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise

        return wrapper

    return decorator


class Flaky:
    """Lève ConnectionError lors des `failures` premiers appels, puis renvoie "ok"."""

    def __init__(self, failures):
        self.failures = failures
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self.calls <= self.failures:
            raise ConnectionError(f"failure {self.calls}")
        return "ok"


def on_fails_twice(decorator, times):
    target = Flaky(2)
    return decorator(target)(), target.calls


def on_never_fails(decorator, times):
    target = Flaky(0)
    return decorator(target)(), target.calls


def attempts_on_permanent_failure(decorator, times):
    target = Flaky(100)
    try:
        decorator(target)()
    except ConnectionError:
        pass
    return target.calls


def factory_only(decorator, times):
    return "retry(times) n'a pas levé d'exception"


TEST_CASES = [
    {"args": (3,), "then": on_fails_twice, "expected": ("ok", 3)},
    {"args": (5,), "then": on_fails_twice, "expected": ("ok", 3), "note": "on s'arrête au premier succès"},
    {"args": (1,), "then": on_never_fails, "expected": ("ok", 1), "note": "succès immédiat : un seul appel"},
    {"args": (2,), "then": on_fails_twice, "raises": ConnectionError, "note": "essais épuisés : l'exception remonte"},
    {"args": (3,), "then": attempts_on_permanent_failure, "expected": 3, "note": "exactement `times` essais"},
    {"args": (0,), "then": factory_only, "raises": ValueError, "note": "times < 1 : erreur dès retry(times)"},
]
