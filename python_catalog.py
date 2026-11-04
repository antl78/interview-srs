"""Catalogue des exercices Python : lit les fichiers de python_exercises/
et en tire la liste des exercices (pour les menus et la file de révision)
ainsi que, pour un exercice, sa fonction de référence et ses cas de test.

Format d'un exercice : voir le doc projet python_exercise_spec.md.

    python_exercises/
        <theme>/
            _theme.py                       THEME = {"level": ..., "label": ...}
            01_<exercise_name>.py           META, fonction de référence, TEST_CASES

Les fichiers sont la seule source de vérité : rien n'est copié dans la base
de contenu, le catalogue est relu au démarrage de l'app."""

import importlib.util
import inspect
import re
from pathlib import Path
from types import ModuleType

import pandas as pd

EXERCISES_DIR = Path(__file__).parent / "python_exercises"

# "01_top_k_frequent_words.py" -> position 1, nom "top_k_frequent_words"
EXERCISE_FILE_PATTERN = re.compile(r"^(\d{2})_([a-z][a-z0-9_]*)\.py$")

REQUIRED_META_KEYS = {"title", "prompt", "function"}
CATALOG_COLUMNS = [
    "exercise_name", "theme", "level", "theme_label", "position",
    "title", "prompt", "hints", "function_name", "starter_code", "path",
]


class ExerciseFormatError(ValueError):
    """Fichier d'exercice ou de thème qui ne respecte pas la spec."""


def load_module(path: Path) -> ModuleType:
    """Importe un fichier .py hors de tout package, sous un nom unique."""
    module_name = "pyex_" + "_".join(path.with_suffix("").parts[-2:])
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_theme(theme_dir: Path) -> dict:
    """Lit _theme.py : niveau (1 à 6, None pour un hors-série) et libellé."""
    theme_file = theme_dir / "_theme.py"
    if not theme_file.exists():
        raise ExerciseFormatError(f"{theme_dir.name} : _theme.py manquant")
    theme = getattr(load_module(theme_file), "THEME", None)
    if not isinstance(theme, dict) or "label" not in theme or "level" not in theme:
        raise ExerciseFormatError(
            f"{theme_file} : THEME doit être un dict avec 'level' et 'label'"
        )
    return theme


def get_reference_function(module: ModuleType, path: Path):
    """Fonction de référence désignée par META['function']."""
    meta = getattr(module, "META", None)
    if not isinstance(meta, dict) or not REQUIRED_META_KEYS <= meta.keys():
        raise ExerciseFormatError(
            f"{path} : META doit contenir {sorted(REQUIRED_META_KEYS)}"
        )
    function = getattr(module, meta["function"], None)
    if not inspect.isfunction(function):
        raise ExerciseFormatError(
            f"{path} : la fonction {meta['function']!r} n'existe pas"
        )
    return function


def build_starter_code(function) -> str:
    """Code pré-rempli dans l'éditeur : la signature seule, corps vide."""
    return f"def {function.__name__}{inspect.signature(function)}:\n    ...\n"


def load_exercise(path: Path) -> dict:
    """Charge un fichier d'exercice et vérifie son format."""
    module = load_module(path)
    function = get_reference_function(module, path)
    test_cases = getattr(module, "TEST_CASES", None)
    if not isinstance(test_cases, list) or not test_cases:
        raise ExerciseFormatError(f"{path} : TEST_CASES doit être une liste non vide")
    for i, case in enumerate(test_cases):
        if "args" not in case or ("expected" in case) == ("raises" in case):
            raise ExerciseFormatError(
                f"{path} : cas {i} — 'args' et exactement un de "
                "'expected' / 'raises' sont requis"
            )
        then = case.get("then")
        if then is not None and (
            not inspect.isfunction(then) or then.__name__ == "<lambda>"
        ):
            raise ExerciseFormatError(
                f"{path} : cas {i} — 'then' doit être une fonction nommée"
            )
    return {
        "meta": module.META,
        "function": function,
        "test_cases": test_cases,
        "reference_source": inspect.getsource(function),
    }


def load_catalog(exercises_dir: Path = EXERCISES_DIR) -> pd.DataFrame:
    """Un exercice par ligne, trié par niveau, thème puis position. Lève
    ExerciseFormatError au premier fichier invalide (mieux vaut une erreur
    franche qu'un exercice qui disparaît sans prévenir)."""
    rows = []
    seen_names: dict[str, Path] = {}
    if exercises_dir.is_dir():
        for theme_dir in sorted(p for p in exercises_dir.iterdir() if p.is_dir()):
            if theme_dir.name.startswith(("_", ".")):
                continue
            theme = load_theme(theme_dir)
            for path in sorted(theme_dir.glob("*.py")):
                if path.name == "_theme.py":
                    continue
                match = EXERCISE_FILE_PATTERN.match(path.name)
                if not match:
                    raise ExerciseFormatError(
                        f"{path} : nom attendu NN_nom_en_snake_case.py"
                    )
                name = match.group(2)
                if name in seen_names:
                    raise ExerciseFormatError(
                        f"{path} : nom déjà utilisé par {seen_names[name]}"
                    )
                seen_names[name] = path
                exercise = load_exercise(path)
                meta = exercise["meta"]
                rows.append({
                    "exercise_name": name,
                    "theme": theme_dir.name,
                    "level": theme["level"],
                    "theme_label": theme["label"],
                    "position": int(match.group(1)),
                    "title": meta["title"],
                    "prompt": meta["prompt"],
                    "hints": list(meta.get("hints", [])),
                    "function_name": exercise["function"].__name__,
                    "starter_code": build_starter_code(exercise["function"]),
                    "path": str(path),
                })
    catalog = pd.DataFrame(rows, columns=CATALOG_COLUMNS)
    # Les hors-séries (level None) passent après les niveaux numérotés.
    catalog["level_order"] = catalog["level"].fillna(99)
    return (
        catalog.sort_values(["level_order", "theme", "position"])
        .drop(columns="level_order")
        .reset_index(drop=True)
    )
