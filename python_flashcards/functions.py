THEME = {"level": 2, "label": "Fonctions"}

CARDS = [
    {
        "name": "mutable_default_argument",
        "question": "Pourquoi `def add(x, items=[])` est-il un piège ?",
        "answer": (
            "La valeur par défaut est évaluée **une seule fois**, à l'exécution "
            "du `def`, pas à chaque appel. La même liste est donc partagée par "
            "tous les appels qui ne passent pas `items`.\n\n"
            "Idiome : `items=None`, puis `if items is None: items = []` dans le corps."
        ),
        "example": (
            "def add(x, items=[]):\n"
            "    items.append(x)\n"
            "    return items\n"
            "\n"
            "print(add(1))\n"
            "print(add(2))\n"
            "print(add.__defaults__)\n"
        ),
        "output": "[1]\n[1, 2]\n([1, 2],)",
    },
    {
        "name": "argument_passing",
        "question": (
            "Une fonction reçoit une liste. L'appelant voit-il le changement "
            "avec `lst.append(4)` ? Et avec `lst = lst + [4]` ?"
        ),
        "answer": (
            "Python passe une **référence vers l'objet** (ni par valeur, ni par "
            "référence au sens C++).\n\n"
            "- **Muter** l'objet (`append`, `lst[0] = ...`, `+=` sur une liste) : "
            "visible par l'appelant.\n"
            "- **Réaffecter** le nom (`lst = ...`) : le nom local pointe vers un "
            "nouvel objet, l'appelant ne voit rien."
        ),
        "example": (
            "def mutate(lst):\n"
            "    lst.append(4)\n"
            "\n"
            "def rebind(lst):\n"
            "    lst = lst + [5]\n"
            "\n"
            "nums = [1, 2, 3]\n"
            "mutate(nums)\n"
            "rebind(nums)\n"
            "print(nums)\n"
        ),
        "output": "[1, 2, 3, 4]",
    },
    {
        "name": "extended_unpacking",
        "question": "Que valent `first`, `middle` et `last` après `first, *middle, last = (1, 2, 3, 4, 5)` ?",
        "answer": (
            "`first = 1`, `middle = [2, 3, 4]`, `last = 5`.\n\n"
            "La variable étoilée est **toujours une liste** (même si la source "
            "est un tuple ou une chaîne, et même vide). Une seule étoile par "
            "affectation ; s'il manque des éléments pour les noms sans étoile : `ValueError`."
        ),
        "example": (
            "first, *middle, last = (1, 2, 3, 4, 5)\n"
            "print(first, middle, last)\n"
            "head, *tail = \"ab\"\n"
            "print(head, tail)\n"
            "a, *b, c = [1, 2]\n"
            "print(a, b, c)\n"
        ),
        "output": "1 [2, 3, 4] 5\na ['b']\n1 [] 2",
    },
]
