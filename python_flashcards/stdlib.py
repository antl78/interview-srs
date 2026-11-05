THEME = {"level": 3, "label": "functools et collections"}

CARDS = [
    {
        "name": "functools_partial",
        "question": "Que fait `functools.partial`, et à quoi sert-il ?",
        "answer": (
            "Il crée un appelable dont certains arguments sont **déjà fixés** : "
            "`partial(f, a, k=v)(x)` équivaut à `f(a, x, k=v)`.\n\n"
            "Utile pour passer une fonction « à un paramètre près » à `map`, à "
            "`sorted(key=...)` ou à un callback, à la place d'une lambda."
        ),
        "example": (
            "from functools import partial\n"
            "\n"
            "def power(base, exponent):\n"
            "    return base ** exponent\n"
            "\n"
            "square = partial(power, exponent=2)\n"
            "print(square(5))\n"
            "print(list(map(partial(power, 2), [1, 2, 3])))\n"
            "print(partial(int, base=2)(\"101\"))\n"
        ),
        "output": "25\n[2, 4, 8]\n5",
    },
    {
        "name": "lru_cache_hashable_args",
        "question": "Pourquoi une fonction décorée par `@cache` (ou `@lru_cache`) lève-t-elle `TypeError` quand on lui passe une `list` ?",
        "answer": (
            "Le cache est un **dict** dont la clé est construite à partir des "
            "arguments : ils doivent tous être **hashables**. Passer un `tuple` "
            "(ou un `frozenset`) au lieu d'une `list` (ou d'un `set`).\n\n"
            "À savoir aussi : `@cache` = `@lru_cache(maxsize=None)`, cache illimité ; "
            "`f.cache_info()` donne hits et misses."
        ),
        "example": (
            "from functools import cache\n"
            "\n"
            "@cache\n"
            "def total(numbers):\n"
            "    return sum(numbers)\n"
            "\n"
            "try:\n"
            "    total([1, 2, 3])\n"
            "except TypeError:\n"
            "    print(\"TypeError\")\n"
            "print(total((1, 2, 3)))\n"
            "total((1, 2, 3))\n"
            "print(total.cache_info().hits)\n"
        ),
        "output": "TypeError\n6\n1",
    },
    {
        "name": "namedtuple",
        "question": "Qu'apporte `collections.namedtuple` par rapport à un tuple simple ?",
        "answer": (
            "Des **champs nommés** (`p.x` plutôt que `p[0]`) et un `repr` lisible, "
            "tout en restant un tuple : immuable, hashable, dépaquetable, aussi léger. "
            "`_replace` renvoie une copie modifiée.\n\n"
            "Pour des valeurs par défaut typées ou des méthodes : `typing.NamedTuple` ; "
            "pour un objet mutable : `@dataclass`."
        ),
        "example": (
            "from collections import namedtuple\n"
            "\n"
            "Point = namedtuple(\"Point\", [\"x\", \"y\"])\n"
            "p = Point(1, 2)\n"
            "print(p, p.x, p[1])\n"
            "x, y = p\n"
            "print(p._replace(y=5), p == (1, 2))\n"
        ),
        "output": "Point(x=1, y=2) 1 2\nPoint(x=1, y=5) True",
    },
    {
        "name": "sort_stability",
        "question": "Le tri Python est-il stable ? Dans quel ordre `Counter.most_common` renvoie-t-il les ex aequo ?",
        "answer": (
            "Oui : `sorted` et `list.sort` sont **stables**, les éléments égaux "
            "pour la clé gardent leur ordre d'origine. On peut donc trier en "
            "plusieurs passes (clé secondaire d'abord, principale ensuite).\n\n"
            "`most_common` repose sur ce tri : les ex aequo restent dans l'**ordre "
            "de première apparition**. Pour un autre départage, clé tuple : "
            "`key=lambda kv: (-kv[1], kv[0])`."
        ),
        "example": (
            "from collections import Counter\n"
            "\n"
            "people = [(\"Bob\", 30), (\"Alice\", 25), (\"Chloé\", 30), (\"David\", 25)]\n"
            "print(sorted(people, key=lambda p: p[1]))\n"
            "\n"
            "counts = Counter(\"cbabc\")\n"
            "print(counts.most_common(2))\n"
            "print(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:2])\n"
        ),
        "output": (
            "[('Alice', 25), ('David', 25), ('Bob', 30), ('Chloé', 30)]\n"
            "[('c', 2), ('b', 2)]\n"
            "[('b', 2), ('c', 2)]"
        ),
    },
]
