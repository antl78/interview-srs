THEME = {"level": 3, "label": "Exceptions"}

CARDS = [
    {
        "name": "try_except_else_finally",
        "question": "Quand s'exécutent les blocs `else` et `finally` d'un `try` ?",
        "answer": (
            "`else` : seulement si le `try` n'a **levé aucune exception**. On y met "
            "la suite du traitement, pour ne pas attraper par erreur ses propres "
            "exceptions dans le `except`.\n\n"
            "`finally` : **toujours**, même après un `return` ou une exception non "
            "attrapée. C'est la place du nettoyage."
        ),
        "example": (
            "def parse(text):\n"
            "    try:\n"
            "        value = int(text)\n"
            "    except ValueError:\n"
            "        print(\"except\")\n"
            "        return None\n"
            "    else:\n"
            "        print(\"else\")\n"
            "        return value\n"
            "    finally:\n"
            "        print(\"finally\")\n"
            "\n"
            "print(parse(\"42\"))\n"
            "print(parse(\"x\"))\n"
        ),
        "output": "else\nfinally\n42\nexcept\nfinally\nNone",
    },
    {
        "name": "raise_from",
        "question": "À quoi sert `raise NewError(...) from err` ?",
        "answer": (
            "À **chaîner** les exceptions : l'exception d'origine est gardée dans "
            "`__cause__` et affichée dans la traceback (« The above exception was "
            "the direct cause… »).\n\n"
            "Utile pour traduire une erreur technique en erreur métier sans perdre "
            "l'origine. `raise ... from None` masque la cause."
        ),
        "example": (
            "class ConfigError(Exception):\n"
            "    pass\n"
            "\n"
            "def load_port(settings):\n"
            "    try:\n"
            "        return int(settings[\"port\"])\n"
            "    except KeyError as err:\n"
            "        raise ConfigError(\"port manquant\") from err\n"
            "\n"
            "try:\n"
            "    load_port({})\n"
            "except ConfigError as e:\n"
            "    print(repr(e))\n"
            "    print(repr(e.__cause__))\n"
        ),
        "output": "ConfigError('port manquant')\nKeyError('port')",
    },
    {
        "name": "custom_exception",
        "question": "Comment définir une exception personnalisée, et de quelle classe hériter ?",
        "answer": (
            "Une classe qui hérite d'**`Exception`**, jamais de `BaseException` "
            "(réservée à `KeyboardInterrupt`, `SystemExit`…).\n\n"
            "Bonne pratique : une classe de base par projet, puis des sous-classes. "
            "`except AppError` attrape alors toute la famille, puisque `except` "
            "accepte les sous-classes."
        ),
        "example": (
            "class AppError(Exception):\n"
            "    \"\"\"Base des erreurs de l'application.\"\"\"\n"
            "\n"
            "class NotFoundError(AppError):\n"
            "    def __init__(self, key):\n"
            "        super().__init__(f\"{key!r} introuvable\")\n"
            "        self.key = key\n"
            "\n"
            "try:\n"
            "    raise NotFoundError(\"user_42\")\n"
            "except AppError as e:\n"
            "    print(type(e).__name__, \"|\", e, \"|\", e.key)\n"
        ),
        "output": "NotFoundError | 'user_42' introuvable | user_42",
    },
]
