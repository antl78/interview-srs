THEME = {"level": 4, "label": "Context managers"}

CARDS = [
    {
        "name": "exit_return_true",
        "question": "Que se passe-t-il si `__exit__` renvoie `True` ?",
        "answer": (
            "`__exit__(exc_type, exc, tb)` reçoit l'exception levée dans le bloc "
            "`with` (ou trois `None`). S'il renvoie une valeur **vraie**, "
            "l'exception est **supprimée** et l'exécution reprend après le `with`. "
            "S'il renvoie `None` ou `False` (cas habituel), elle se propage.\n\n"
            "Renvoyer `True` sans condition avale toutes les erreurs : filtrer sur `exc_type`."
        ),
        "example": (
            "class Ignore:\n"
            "    def __init__(self, *types):\n"
            "        self.types = types\n"
            "    def __enter__(self):\n"
            "        return self\n"
            "    def __exit__(self, exc_type, exc, tb):\n"
            "        return exc_type is not None and issubclass(exc_type, self.types)\n"
            "\n"
            "with Ignore(KeyError):\n"
            "    {}[\"missing\"]\n"
            "    print(\"jamais affiché\")\n"
            "print(\"après le with\")\n"
            "\n"
            "try:\n"
            "    with Ignore(KeyError):\n"
            "        1 / 0\n"
            "except ZeroDivisionError:\n"
            "    print(\"ZeroDivisionError propagée\")\n"
        ),
        "output": "après le with\nZeroDivisionError propagée",
    },
    {
        "name": "contextmanager_try_finally",
        "question": "Pourquoi entourer le `yield` d'un `try / finally` dans un `@contextmanager` ?",
        "answer": (
            "Une exception levée dans le bloc `with` est **relancée au niveau du "
            "`yield`**. Sans `try / finally`, le code placé après le `yield` (le "
            "nettoyage) ne s'exécute pas.\n\n"
            "Avec `finally`, le nettoyage a toujours lieu, et l'exception continue "
            "de se propager (sauf si on l'attrape avec un `except`)."
        ),
        "example": (
            "from contextlib import contextmanager\n"
            "\n"
            "@contextmanager\n"
            "def fragile():\n"
            "    print(\"ouverture\")\n"
            "    yield\n"
            "    print(\"fermeture\")\n"
            "\n"
            "@contextmanager\n"
            "def robust():\n"
            "    print(\"ouverture\")\n"
            "    try:\n"
            "        yield\n"
            "    finally:\n"
            "        print(\"fermeture\")\n"
            "\n"
            "for manager in (fragile, robust):\n"
            "    try:\n"
            "        with manager():\n"
            "            raise ValueError\n"
            "    except ValueError:\n"
            "        print(\"ValueError\")\n"
        ),
        "output": "ouverture\nValueError\nouverture\nfermeture\nValueError",
    },
]
