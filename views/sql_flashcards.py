"""Page Mémocards SQL : question/réponse simple pour mémoriser la syntaxe.
Pas encore branchée sur la répétition espacée (REVIEW_INTERVALS) —
volontairement minimal pour l'instant, le temps de voir si le contenu et
le format conviennent."""

import random

import streamlit as st

from srs_core import get_connection, theme_menu

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


def reveal_flashcard_answer() -> None:
    """Callback (on_click) du bouton Afficher la réponse."""
    st.session_state["flashcard_revealed"] = True


def next_flashcard(card_names: list) -> None:
    """Callback (on_click) du bouton Carte suivante : tire une nouvelle
    carte au hasard (différente de la précédente s'il y en a plusieurs) et
    masque la réponse."""
    previous = st.session_state.get("flashcard_current")
    choices = [c for c in card_names if c != previous] or card_names
    st.session_state["flashcard_current"] = random.choice(choices)
    st.session_state["flashcard_revealed"] = False


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

    card_names = list(flashcards_df["card_name"])

    # Changement de thème (ou premier passage) : tirage initial au
    # hasard, mémorisé dans session_state pour rester stable entre les
    # reruns tant qu'on reste sur la même carte.
    if st.session_state.get("flashcard_theme_loaded") != flashcard_theme:
        st.session_state["flashcard_current"] = random.choice(card_names)
        st.session_state["flashcard_revealed"] = False
        st.session_state["flashcard_theme_loaded"] = flashcard_theme

    card = flashcards_df[
        flashcards_df["card_name"] == st.session_state["flashcard_current"]
    ].iloc[0]

    nb_cards = len(card_names)
    st.subheader(f"Mémocard — {flashcard_theme} ({nb_cards} carte{'s' if nb_cards > 1 else ''})")
    st.write(card["question"])

    if st.session_state.get("flashcard_revealed"):
        st.success(card["answer"])
        if card["example"]:
            st.code(card["example"], language="sql")
    else:
        st.button("Afficher la réponse", on_click=reveal_flashcard_answer)

    st.button("Carte suivante ➡️", on_click=next_flashcard, args=(card_names,))
