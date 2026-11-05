THEME = {"level": 4, "label": "Closures et décorateurs"}

CARDS = [
    {
        "name": "closure_cells",
        "question": "Où une closure garde-t-elle les variables de la fonction englobante ? Quel piège en découle ?",
        "answer": (
            "Dans des **cellules** : `f.__closure__` (tuple d'objets `cell`), avec "
            "les noms dans `f.__code__.co_freevars`.\n\n"
            "La cellule pointe vers la **variable**, pas vers sa valeur au moment "
            "de la création : c'est le *late binding*. `[lambda: i for i in range(3)]` "
            "renvoie trois fois `2`. Correction : figer la valeur avec un argument "
            "par défaut, `lambda i=i: i`."
        ),
        "example": (
            "def make_adder(n):\n"
            "    def add(x):\n"
            "        return x + n\n"
            "    return add\n"
            "\n"
            "add5 = make_adder(5)\n"
            "print(add5.__code__.co_freevars, add5.__closure__[0].cell_contents)\n"
            "\n"
            "late = [lambda: i for i in range(3)]\n"
            "fixed = [lambda i=i: i for i in range(3)]\n"
            "print([f() for f in late], [f() for f in fixed])\n"
        ),
        "output": "('n',) 5\n[2, 2, 2] [0, 1, 2]",
    },
    {
        "name": "decorator_stacking_order",
        "question": "Dans quel ordre s'appliquent deux décorateurs empilés, `@a` puis `@b`, au-dessus de `def f` ?",
        "answer": (
            "L'application se fait **de bas en haut** : `f = a(b(f))`.\n\n"
            "À l'appel, le wrapper de `a` (le plus haut) s'exécute donc en premier, "
            "puis celui de `b`, puis `f`. Le code « après » se déroule dans l'ordre inverse."
        ),
        "example": (
            "def tag(name):\n"
            "    def decorator(func):\n"
            "        def wrapper():\n"
            "            print(f\"{name} avant\")\n"
            "            result = func()\n"
            "            print(f\"{name} après\")\n"
            "            return result\n"
            "        return wrapper\n"
            "    return decorator\n"
            "\n"
            "@tag(\"a\")\n"
            "@tag(\"b\")\n"
            "def f():\n"
            "    print(\"f\")\n"
            "\n"
            "f()\n"
        ),
        "output": "a avant\nb avant\nf\nb après\na après",
    },
    {
        "name": "functools_wraps",
        "question": "Pourquoi utiliser `@functools.wraps(func)` dans un décorateur ?",
        "answer": (
            "Sans lui, la fonction décorée prend le nom et la docstring du "
            "**wrapper** (`wrapper`, `None`) : logs, traceback, `help()` et tests "
            "deviennent trompeurs.\n\n"
            "`wraps` copie `__name__`, `__qualname__`, `__doc__`, `__module__` et "
            "`__dict__`, et ajoute `__wrapped__`, qui donne accès à la fonction "
            "d'origine (et à sa vraie signature via `inspect.signature`)."
        ),
        "example": (
            "from functools import wraps\n"
            "\n"
            "def plain(func):\n"
            "    def wrapper(*args, **kwargs):\n"
            "        return func(*args, **kwargs)\n"
            "    return wrapper\n"
            "\n"
            "def wrapped(func):\n"
            "    @wraps(func)\n"
            "    def wrapper(*args, **kwargs):\n"
            "        return func(*args, **kwargs)\n"
            "    return wrapper\n"
            "\n"
            "@plain\n"
            "def add(a, b):\n"
            "    \"\"\"Additionne a et b.\"\"\"\n"
            "    return a + b\n"
            "\n"
            "@wrapped\n"
            "def mul(a, b):\n"
            "    \"\"\"Multiplie a et b.\"\"\"\n"
            "    return a * b\n"
            "\n"
            "print(add.__name__, add.__doc__)\n"
            "print(mul.__name__, mul.__doc__)\n"
            "print(mul.__wrapped__(3, 4))\n"
        ),
        "output": "wrapper None\nmul Multiplie a et b.\n12",
    },
]
