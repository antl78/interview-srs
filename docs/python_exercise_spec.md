# Spec du format d'exercice Python (interview-srs)

Ce document suffit, seul, pour écrire des exercices Python directement intégrables. Toute conversation de niveau part d'ici.

## 1. Emplacement et nommage

```
python_exercises/
  <theme>/                      # snake_case, ex. idiomatic, stdlib, generators
    _theme.py                   # niveau et libellé du thème
    01_<exercise_name>.py       # un fichier par exercice
    02_<exercise_name>.py
```

- `<exercise_name>` est en snake_case, en anglais, et **unique sur tout le Python** (pas seulement dans le thème). Il sert de clé dans la progression (`track = 'python'`).
- Le préfixe `NN_`, sur deux chiffres, donne l'ordre des exercices dans le thème : du plus simple au plus difficile.
- Les dossiers commençant par `_` ou `.` sont ignorés.

`_theme.py` :

```python
THEME = {"level": 2, "label": "Python idiomatique"}
```

`level` vaut de 1 à 6, ou `None` pour un hors-série (dates/pandas, algorithmes classiques). Les hors-séries s'affichent après les niveaux numérotés.

## 2. Contenu d'un fichier d'exercice

Trois éléments, dans cet ordre : `META`, la fonction de référence, `TEST_CASES`.

```python
META = {
    "title": "Second largest",            # anglais, Title Case
    "function": "second_largest",         # nom de la fonction à écrire
    "prompt": "Renvoie ... Lève une `ValueError` si ...",   # français, Markdown
    "hints": ["...", "..."],              # facultatif, du plus vague au plus précis
}


def second_largest(numbers: list[int]) -> int:
    """Reference solution."""
    ...


TEST_CASES = [
    {"args": ([3, 1, 4, 1, 5],), "expected": 4},
    {"args": ([7, 7, 7],), "raises": ValueError, "note": "une seule valeur distincte"},
]
```

- **La signature de la fonction de référence est celle qu'on impose.** L'éditeur est pré-rempli avec `def <nom><signature>:` suivi de `...`. Les noms de paramètres et les type hints font donc partie de l'énoncé.
- Des fonctions auxiliaires sont permises dans le fichier. Seule `META["function"]` est appelée par les tests.
- Pas d'import au niveau du module, sauf s'il est nécessaire à la solution (`from collections import Counter`…).

## 3. Cas de test

Chaque cas est un `dict` :

| Clé | Obligatoire | Rôle |
|---|---|---|
| `args` | oui | tuple des arguments positionnels (attention : `("x",)` pour un seul argument) |
| `kwargs` | non | dict des arguments nommés |
| `expected` | un des deux | valeur de retour attendue |
| `raises` | un des deux | classe d'exception attendue (`ValueError`), sous-classes acceptées |
| `compare` | non | `"exact"` (défaut), `"unordered"`, `"approx"` |
| `note` | non | libellé affiché ; **obligatoire sur les cas limites** |

Les arguments sont copiés (`deepcopy`) avant chaque appel : si la fonction modifie ses entrées, cela ne fausse ni les autres cas ni l'affichage.

## 4. Règles de comparaison

- **`exact`** : `type(got) is type(expected)` et `got == expected`. Renvoyer un `tuple` au lieu d'une `list`, un `int` au lieu d'un `float`, ou `True` au lieu de `1` est un échec, avec le message « type X au lieu de Y ». Le type n'est vérifié qu'au premier niveau.
- **`unordered`** : même type, mêmes éléments avec le même nombre de doublons, ordre indifférent. À utiliser quand l'énoncé dit « l'ordre n'a pas d'importance » ou quand le résultat vient d'un set.
- **`approx`** : tolérance de 1e-9 (relative et absolue) sur les nombres, récursive sur les `list`, `tuple` et `dict`. `int` et `float` y sont interchangeables. Obligatoire dès qu'un flottant est calculé.
- **`raises`** : réussi si l'exception levée est une instance de la classe attendue. Une autre exception, ou aucune exception, est un échec.

Prévu plus tard, pas encore implémenté :
- `"compare": "dataframe"` pour le hors-série pandas (`pd.testing.assert_frame_equal`) ;
- un `"setup"` qui instancie une classe, pour le niveau 5.

## 5. Exécution

- Le code de l'utilisateur tourne dans un processus séparé (`python -I python_runner.py`), avec un délai maximal de 5 s pour l'ensemble des cas.
- Les `print` sont capturés par cas de test et affichés dans le détail. Ils ne cassent pas le résultat.
- Une erreur de syntaxe ou une fonction absente donne un message global, et aucun cas n'est lancé.
- Sécurité : ce processus protège l'app des boucles infinies et des plantages, pas d'un code malveillant. C'est acceptable uniquement parce que l'app est privée.

## 6. Conventions de rédaction

- **Énoncé** : en français, 1 à 3 phrases. Il nomme les paramètres entre backticks, dit ce qui est renvoyé et précise les cas particuliers (vide, doublons, exception). Le niveau d'entretien vient du choix du bon outil, pas d'un énoncé obscur.
- **Cas de test** : de 4 à 6 par exercice, dont au moins 2 cas limites annotés par `note` (entrée vide, un seul élément, doublons, négatifs, casse, exception…). Les cas doivent faire échouer les solutions naïves typiques.
- **Solution de référence** : idiomatique, avec type hints et la docstring `"""Reference solution."""`. C'est elle qu'on lit dans l'onglet Solution, elle doit donc montrer la bonne pratique du niveau : `Counter` plutôt qu'une boucle au niveau 3, par exemple.
- **Indices** : au plus 3. Le premier oriente sans rien donner, le dernier peut nommer l'outil à utiliser.
- **Difficulté** : un exercice se résout en 5 à 15 minutes. Au-delà, il faut le découper.

## 7. Vérification avant intégration

```
uv run pytest
```

- `tests/test_python_exercises.py` vérifie que chaque fichier respecte le format, que chaque solution de référence passe tous ses cas et qu'il y a au moins un cas limite annoté.
- `tests/test_python_runner.py` vérifie le comportement du runner : timeout, erreurs, `print`, mutation des entrées, accents.

Un exercice dont le test échoue n'est pas intégré.

## 8. Exemple complet

`python_exercises/idiomatic/01_top_k_frequent_words.py`

```python
META = {
    "title": "Top K frequent words",
    "function": "top_k_frequent_words",
    "prompt": (
        "Renvoie les `k` mots les plus fréquents de `text` (insensible à la "
        "casse), du plus fréquent au moins fréquent, les ex aequo étant "
        "départagés par ordre alphabétique. Lève une `ValueError` si `k` "
        "est négatif."
    ),
    "hints": [
        "Compte d'abord, trie ensuite.",
        "sorted() accepte une clé qui renvoie un tuple : (-count, word).",
    ],
}


def top_k_frequent_words(text: str, k: int) -> list[str]:
    """Reference solution."""
    if k < 0:
        raise ValueError("k must be non-negative")
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return sorted(counts, key=lambda w: (-counts[w], w))[:k]


TEST_CASES = [
    {"args": ("b a b c a b", 2), "expected": ["b", "a"]},
    {"args": ("x y z", 2), "expected": ["x", "y"], "note": "ex aequo : ordre alphabétique"},
    {"args": ("A a B", 1), "expected": ["a"], "note": "insensible à la casse"},
    {"args": ("", 3), "expected": [], "note": "texte vide"},
    {"args": ("a b", 5), "expected": ["a", "b"], "note": "k plus grand que le nombre de mots"},
    {"args": ("a", -1), "raises": ValueError, "note": "k négatif"},
]
```
