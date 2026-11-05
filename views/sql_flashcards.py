"""Page Mémocards SQL : question/réponse simple pour mémoriser la syntaxe.
Affichage commun avec les mémocards Python (srs_core.show_flashcards).
Pas encore branchée sur la répétition espacée (REVIEW_INTERVALS) —
volontairement minimal pour l'instant, le temps de voir si le contenu et
le format conviennent."""

import streamlit as st

from srs_core import get_connection, show_flashcards, theme_menu

con = get_connection()

FLASHCARD_THEME_LEVELS = {
    "Niveau 1 · Fondamentaux": ["null_filtering", "strings", "sets"],
    "Niveau 2 · Joins, CTE, CRUD": ["joins", "cte", "crud"],
    "Niveau 3 · Agrégations, CASE WHEN, GROUPING SETS": [
        "aggregates", "stats", "case_when", "grouping_sets",
    ],
    "Niveau 4 · Agrégations conditionnelles, dates": [
        "conditional_aggregation", "dates",
    ],
    "Niveau 5 · Window functions": ["window_functions"],
}


with st.sidebar:
    flashcard_themes = con.execute(
        "SELECT DISTINCT theme FROM flashcards ORDER BY theme"
    ).df()["theme"].tolist()

    st.markdown("**Thème à réviser ?**")
    flashcard_theme = theme_menu(
        flashcard_themes, FLASHCARD_THEME_LEVELS, "selected_flashcard_theme"
    )

if not flashcard_themes:
    st.info("Aucune mémocard disponible pour l'instant.")
elif not flashcard_theme:
    st.info("Sélectionnez un thème dans la barre à gauche")
else:
    flashcards_df = con.execute(
        "SELECT * FROM flashcards WHERE theme = ? ORDER BY card_name",
        [flashcard_theme],
    ).df()

    show_flashcards(flashcards_df, flashcard_theme, state_prefix="flashcard", language="sql")
