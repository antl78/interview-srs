THEME = {"level": 3, "label": "Portée des variables"}

CARDS = [
    {
        "name": "legb_rule",
        "question": "Dans quel ordre Python cherche-t-il un nom (règle LEGB) ?",
        "answer": (
            "**L**ocal (fonction en cours) → **E**nclosing (fonctions englobantes) "
            "→ **G**lobal (module) → **B**uilt-in (`len`, `print`…). Le premier "
            "trouvé l'emporte.\n\n"
            "D'où le masquage : `list = [...]` au niveau du module cache le "
            "built-in `list` dans tout le module."
        ),
        "example": (
            "x = \"global\"\n"
            "\n"
            "def outer():\n"
            "    x = \"enclosing\"\n"
            "    def inner():\n"
            "        return x\n"
            "    return inner()\n"
            "\n"
            "def shadow():\n"
            "    len = 10\n"
            "    return len\n"
            "\n"
            "print(outer(), x)\n"
            "print(shadow(), len(\"abc\"))\n"
        ),
        "output": "enclosing global\n10 3",
    },
    {
        "name": "unbound_local_error",
        "question": (
            "Pourquoi `inc()` lève-t-il `UnboundLocalError` ?\n\n"
            "```python\ncount = 0\n\ndef inc():\n    count += 1\n```"
        ),
        "answer": (
            "Une affectation (`count += 1`) rend `count` **locale dans toute la "
            "fonction**. C'est décidé à la compilation, avant la première ligne. "
            "La lecture qui précède l'affectation tombe donc sur une locale pas "
            "encore définie.\n\n"
            "Corrections : `global count`, ou mieux, passer la valeur en argument et la renvoyer."
        ),
        "example": (
            "count = 0\n"
            "\n"
            "def inc():\n"
            "    count += 1\n"
            "\n"
            "try:\n"
            "    inc()\n"
            "except UnboundLocalError:\n"
            "    print(\"UnboundLocalError\")\n"
            "\n"
            "def inc_fixed():\n"
            "    global count\n"
            "    count += 1\n"
            "\n"
            "inc_fixed()\n"
            "print(count)\n"
        ),
        "output": "UnboundLocalError\n1",
    },
    {
        "name": "global_vs_nonlocal",
        "question": "Quelle différence entre `global` et `nonlocal` ? Quand sont-ils nécessaires ?",
        "answer": (
            "`global x` : l'affectation vise le `x` du **module**. `nonlocal x` : "
            "elle vise le `x` de la **fonction englobante** la plus proche, qui "
            "doit déjà exister (sinon `SyntaxError`).\n\n"
            "Inutiles pour **lire** une variable ou **muter** un objet "
            "(`lst.append`) : seulement pour la **réaffecter**."
        ),
        "example": (
            "total = 0\n"
            "\n"
            "def make_counter():\n"
            "    count = 0\n"
            "    def step():\n"
            "        global total\n"
            "        nonlocal count\n"
            "        count += 1\n"
            "        total += 10\n"
            "        return count\n"
            "    return step\n"
            "\n"
            "step = make_counter()\n"
            "step()\n"
            "print(step(), total)\n"
        ),
        "output": "2 20",
    },
]
