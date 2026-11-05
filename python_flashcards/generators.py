THEME = {"level": 4, "label": "Générateurs"}

CARDS = [
    {
        "name": "generator_vs_iterator",
        "question": "Quelle différence entre un itérable, un itérateur et un générateur ?",
        "answer": (
            "- **Itérable** : a un `__iter__` qui renvoie un itérateur (`list`, "
            "`str`, `dict`…). On peut le parcourir plusieurs fois.\n"
            "- **Itérateur** : a un `__next__` (qui lève `StopIteration` à la fin) "
            "et un `__iter__` qui renvoie lui-même. Il **s'épuise**.\n"
            "- **Générateur** : itérateur créé par une fonction avec `yield` (ou une "
            "expression `(x for x in ...)`). Il implémente le protocole pour vous "
            "et calcule les valeurs à la demande."
        ),
        "example": (
            "class Countdown:\n"
            "    def __init__(self, start):\n"
            "        self.current = start\n"
            "    def __iter__(self):\n"
            "        return self\n"
            "    def __next__(self):\n"
            "        if self.current <= 0:\n"
            "            raise StopIteration\n"
            "        self.current -= 1\n"
            "        return self.current + 1\n"
            "\n"
            "def countdown(start):\n"
            "    while start > 0:\n"
            "        yield start\n"
            "        start -= 1\n"
            "\n"
            "gen = countdown(3)\n"
            "print(list(Countdown(3)), list(gen), list(gen))\n"
            "nums = [1, 2]\n"
            "print(iter(nums) is nums, iter(gen) is gen)\n"
        ),
        "output": "[3, 2, 1] [3, 2, 1] []\nFalse True",
    },
    {
        "name": "generator_send_close",
        "question": "À quoi servent `send()` et `close()` sur un générateur ?",
        "answer": (
            "`gen.send(v)` reprend le générateur et **fait valoir `v` à l'expression "
            "`yield`** en pause. Le premier appel doit être `next(gen)` (ou "
            "`send(None)`) pour atteindre le premier `yield`.\n\n"
            "`gen.close()` lève **`GeneratorExit`** au point de pause : le `finally` "
            "s'exécute. Le générateur ne doit plus rien produire (laisser remonter "
            "l'exception, ou `return`)."
        ),
        "example": (
            "def averager():\n"
            "    total, count = 0, 0\n"
            "    try:\n"
            "        while True:\n"
            "            value = yield (total / count if count else None)\n"
            "            total += value\n"
            "            count += 1\n"
            "    finally:\n"
            "        print(\"nettoyage\")\n"
            "\n"
            "avg = averager()\n"
            "next(avg)\n"
            "print(avg.send(10))\n"
            "print(avg.send(20))\n"
            "avg.close()\n"
        ),
        "output": "10.0\n15.0\nnettoyage",
    },
]
