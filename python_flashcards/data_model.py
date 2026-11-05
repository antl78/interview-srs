THEME = {"level": 3, "label": "Data model"}

CARDS = [
    {
        "name": "is_vs_equality",
        "question": "Quelle différence entre `is` et `==` ?",
        "answer": (
            "`==` compare les **valeurs** (appelle `__eq__`). `is` compare "
            "l'**identité** : même objet en mémoire (`id(a) == id(b)`).\n\n"
            "`is` sert pour les singletons (`None`, `True`, `False`) ; pour tout le reste, `==`."
        ),
        "example": (
            "a = [1, 2]\n"
            "b = [1, 2]\n"
            "c = a\n"
            "print(a == b, a is b)\n"
            "print(a is c)\n"
            "x = None\n"
            "print(x is None)\n"
        ),
        "output": "True False\nTrue\nTrue",
    },
    {
        "name": "small_int_cache",
        "question": "Pourquoi `a is b` peut-il valoir `True` pour `256` et `False` pour `257` ?",
        "answer": (
            "CPython garde en cache les entiers de **-5 à 256** : tout calcul qui "
            "donne l'un d'eux renvoie le même objet. Au-delà, un nouvel objet est "
            "créé (sauf constantes identiques regroupées par le compilateur dans "
            "un même bloc de code).\n\n"
            "C'est un détail d'implémentation : ne jamais comparer des nombres avec `is`."
        ),
        "example": (
            "a = int(\"256\")\n"
            "b = int(\"256\")\n"
            "print(a is b)\n"
            "c = int(\"257\")\n"
            "d = int(\"257\")\n"
            "print(c is d, c == d)\n"
        ),
        "output": "True\nFalse True",
    },
    {
        "name": "shallow_vs_deep_copy",
        "question": "Quelle différence entre `copy.copy` (ou `list(x)`, `x[:]`) et `copy.deepcopy` ?",
        "answer": (
            "La copie **superficielle** crée un nouveau conteneur mais garde les "
            "**mêmes objets internes** : modifier une sous-liste se voit des deux "
            "côtés. `deepcopy` copie récursivement tout l'arbre.\n\n"
            "Même famille de piège : `[[0] * 3] * 2`, dont les deux lignes sont le même objet."
        ),
        "example": (
            "import copy\n"
            "\n"
            "grid = [[1, 2], [3, 4]]\n"
            "shallow = copy.copy(grid)\n"
            "deep = copy.deepcopy(grid)\n"
            "grid[0].append(99)\n"
            "print(shallow[0])\n"
            "print(deep[0])\n"
            "print(shallow is grid, shallow[0] is grid[0])\n"
        ),
        "output": "[1, 2, 99]\n[1, 2]\nFalse True",
    },
    {
        "name": "hashability",
        "question": "Qu'est-ce qu'un objet hashable, et pourquoi une `list` ne peut-elle pas être une clé de dict ?",
        "answer": (
            "Hashable : `__hash__` **stable pendant toute la vie de l'objet** et "
            "cohérent avec `__eq__` (`a == b` ⇒ `hash(a) == hash(b)`).\n\n"
            "Les immuables le sont (`int`, `str`, `frozenset`, `tuple` de hashables) ; "
            "`list`, `dict` et `set` non, car leur contenu peut changer après "
            "insertion. Solution : convertir (`tuple(lst)`, `frozenset(d.items())`)."
        ),
        "example": (
            "seen = {}\n"
            "try:\n"
            "    seen[[1, 2]] = \"a\"\n"
            "except TypeError as e:\n"
            "    print(type(e).__name__)\n"
            "seen[(1, 2)] = \"a\"\n"
            "seen[frozenset({\"x\": 1}.items())] = \"b\"\n"
            "print(len(seen))\n"
            "try:\n"
            "    hash((1, [2]))\n"
            "except TypeError as e:\n"
            "    print(type(e).__name__, \": tuple contenant une liste\")\n"
        ),
        "output": "TypeError\n2\nTypeError : tuple contenant une liste",
    },
]
