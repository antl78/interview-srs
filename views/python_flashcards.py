"""Page Mémocards Python : question / réponse, avec un exemple de code et
sa sortie. Même fonctionnement que les mémocards SQL (tirage au hasard,
pas encore de répétition espacée). Les cartes sont lues dans
python_flashcards/ (voir python_flashcard_catalog.py)."""

import pandas as pd
import streamlit as st

from python_flashcard_catalog import FLASHCARDS_DIR, load_flashcards
from srs_core import show_flashcards, theme_menu


def flashcard_files_signature() -> tuple:
    """(chemin, date de modification) de chaque fichier de cartes : sert de
    clé au cache, qui se recharge dès qu'un fichier change."""
    return tuple(
        (str(p), p.stat().st_mtime) for p in sorted(FLASHCARDS_DIR.glob("*.py"))
    )


@st.cache_data
def get_flashcards(signature: tuple) -> pd.DataFrame:
    return load_flashcards()


def theme_levels(cards: pd.DataFrame) -> dict:
    """{libellé de niveau : [thèmes]} pour theme_menu, dans l'ordre du
    catalogue (niveaux croissants, hors-séries à la fin)."""
    levels: dict[str, list[str]] = {}
    for row in cards.drop_duplicates("theme").itertuples():
        prefix = "Hors-série" if pd.isna(row.level) else f"Niveau {int(row.level)}"
        levels.setdefault(f"{prefix} · {row.theme_label}", []).append(row.theme)
    return levels


cards = get_flashcards(flashcard_files_signature())
themes = cards["theme"].drop_duplicates().tolist()

with st.sidebar:
    st.markdown("**Thème à réviser ?**")
    flashcard_theme = theme_menu(
        themes, theme_levels(cards), "selected_python_flashcard_theme"
    )

if cards.empty:
    st.info("Aucune mémocard disponible pour l'instant.")
elif not flashcard_theme:
    st.info("Sélectionnez un thème dans la barre à gauche")
else:
    show_flashcards(
        cards[cards["theme"] == flashcard_theme].reset_index(drop=True),
        flashcard_theme,
        state_prefix="python_flashcard",
        language="python",
    )
