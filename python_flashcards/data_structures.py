THEME = {"level": 2, "label": "Structures de données"}

CARDS = [
    {
        "name": "set_membership_complexity",
        "question": "Pourquoi `x in s` est-il en O(1) pour un `set` et en O(n) pour une `list` ?",
        "answer": (
            "Un `set` (comme les clés d'un `dict`) est une **table de hachage** : "
            "`hash(x)` donne directement l'emplacement à regarder, puis `==` "
            "confirme. O(1) en moyenne. Une `list` est parcourue élément par élément.\n\n"
            "Conséquences : les éléments doivent être hashables, et convertir une "
            "fois en `set` (O(n)) est rentable dès qu'on teste l'appartenance plusieurs fois."
        ),
        "example": (
            "class Key:\n"
            "    comparisons = 0\n"
            "    def __init__(self, v):\n"
            "        self.v = v\n"
            "    def __hash__(self):\n"
            "        return hash(self.v)\n"
            "    def __eq__(self, other):\n"
            "        Key.comparisons += 1\n"
            "        return self.v == other.v\n"
            "\n"
            "items = [Key(i) for i in range(1000)]\n"
            "lookup = set(items)\n"
            "target = Key(999)\n"
            "\n"
            "Key.comparisons = 0\n"
            "target in items\n"
            "print(\"list :\", Key.comparisons)\n"
            "Key.comparisons = 0\n"
            "target in lookup\n"
            "print(\"set :\", Key.comparisons)\n"
        ),
        "output": "list : 1000\nset : 1",
    },
    {
        "name": "truthiness",
        "question": "Quelles valeurs sont « falsy » en Python, et quel est le piège de `if not x` ?",
        "answer": (
            "Sont fausses : `None`, `False`, `0` / `0.0`, et les conteneurs vides "
            "(`\"\"`, `[]`, `{}`, `set()`, `()`). Tout le reste est vrai, y compris "
            "`\"0\"`, `\" \"` et `[0]`.\n\n"
            "Piège : `if not value` confond « absent » (`None`) et « vide ou zéro ». "
            "Pour tester l'absence : `if value is None`."
        ),
        "example": (
            "values = [None, 0, 0.0, \"\", \"0\", [], [0], {}, \" \"]\n"
            "print([v for v in values if v])\n"
            "\n"
            "def describe(limit=None):\n"
            "    if not limit:\n"
            "        return \"pas de limite\"\n"
            "    return f\"limite {limit}\"\n"
            "\n"
            "print(describe(0))\n"
        ),
        "output": "['0', [0], ' ']\npas de limite",
    },
]
