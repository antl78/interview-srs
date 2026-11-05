"""Catalogue des mémocards Python : lit les fichiers de python_flashcards/
(un fichier par thème) et renvoie une carte par ligne.

    python_flashcards/
        <theme>.py      THEME = {"level": ..., "label": ...}
                        CARDS = [{"name", "question", "answer", "example", "output"?}]

Comme pour les exercices, les fichiers sont la seule source de vérité :
rien n'est copié dans la base de contenu. L'exemple de chaque carte est
exécuté par les tests (run_example) et sa sortie comparée à "output"."""

import contextlib
import importlib.util
import io
import re
from pathlib import Path
from types import ModuleType

import pandas as pd

FLASHCARDS_DIR = Path(__file__).parent / "python_flashcards"

NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
REQUIRED_CARD_KEYS = {"name", "question", "answer", "example"}
ALLOWED_CARD_KEYS = REQUIRED_CARD_KEYS | {"output"}
CATALOG_COLUMNS = [
    "card_name", "theme", "level", "theme_label", "position",
    "question", "answer", "example", "output", "path",
]


class FlashcardFormatError(ValueError):
    """Fichier de mémocards qui ne respecte pas le format."""


def load_module(path: Path) -> ModuleType:
    """Importe un fichier .py hors de tout package, sous un nom unique."""
    spec = importlib.util.spec_from_file_location(f"pyfc_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_theme_file(path: Path) -> tuple[dict, list[dict]]:
    """Lit THEME et CARDS d'un fichier et vérifie leur format."""
    module = load_module(path)
    theme = getattr(module, "THEME", None)
    if not isinstance(theme, dict) or not {"level", "label"} <= theme.keys():
        raise FlashcardFormatError(f"{path} : THEME doit être un dict avec 'level' et 'label'")
    cards = getattr(module, "CARDS", None)
    if not isinstance(cards, list) or not cards:
        raise FlashcardFormatError(f"{path} : CARDS doit être une liste non vide")
    for i, card in enumerate(cards):
        if not isinstance(card, dict) or not REQUIRED_CARD_KEYS <= card.keys():
            raise FlashcardFormatError(
                f"{path} : carte {i} — clés requises {sorted(REQUIRED_CARD_KEYS)}"
            )
        unknown = card.keys() - ALLOWED_CARD_KEYS
        if unknown:
            raise FlashcardFormatError(f"{path} : carte {i} — clés inconnues {sorted(unknown)}")
        if not NAME_PATTERN.match(card["name"]):
            raise FlashcardFormatError(f"{path} : carte {i} — nom attendu en snake_case")
    return theme, cards


def load_flashcards(flashcards_dir: Path = FLASHCARDS_DIR) -> pd.DataFrame:
    """Une carte par ligne, triée par niveau, thème puis position dans le
    fichier. Lève FlashcardFormatError au premier fichier invalide."""
    rows = []
    seen_names: dict[str, Path] = {}
    if flashcards_dir.is_dir():
        for path in sorted(flashcards_dir.glob("*.py")):
            if path.name.startswith(("_", ".")):
                continue
            if not NAME_PATTERN.match(path.stem):
                raise FlashcardFormatError(f"{path} : nom de fichier attendu en snake_case")
            theme, cards = load_theme_file(path)
            for position, card in enumerate(cards, start=1):
                name = card["name"]
                if name in seen_names:
                    raise FlashcardFormatError(
                        f"{path} : carte {name!r} déjà définie dans {seen_names[name]}"
                    )
                seen_names[name] = path
                rows.append({
                    "card_name": name,
                    "theme": path.stem,
                    "level": theme["level"],
                    "theme_label": theme["label"],
                    "position": position,
                    "question": card["question"],
                    "answer": card["answer"],
                    "example": card["example"],
                    "output": card.get("output"),
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


def run_example(code: str) -> str:
    """Exécute l'exemple d'une carte dans un espace de noms vierge et renvoie
    ce qu'il affiche. Sert aux tests : l'app n'exécute jamais les exemples."""
    buffer = io.StringIO()
    namespace = {"__name__": "__flashcard__"}
    with contextlib.redirect_stdout(buffer):
        exec(compile(code, "<example>", "exec"), namespace)
    return buffer.getvalue()
