"""Point d'entrée de l'app de révision (lancer : streamlit run app.py).

Chaque matière est un groupe de pages dans la navigation de la barre
latérale ; la logique commune (connexion, répétition espacée, menu des
thèmes) est dans srs_core.py. Pour ajouter une matière : créer ses pages
dans views/ et ajouter un groupe ci-dessous."""

import streamlit as st

from srs_core import collapse_sidebar_on_mobile, get_connection

st.set_page_config(page_title="SRS — révisions entretiens", page_icon="🧠")

# Ouvre (et crée au besoin) les bases avant d'afficher quoi que ce soit.
get_connection()

navigation = st.navigation(
    {
        "SQL": [
            st.Page(
                "views/sql_exercises.py",
                title="Exercices SQL",
                icon="📝",
                url_path="sql",
                default=True,
            ),
            st.Page(
                "views/sql_flashcards.py",
                title="Mémocards SQL",
                icon="🃏",
                url_path="sql-memocards",
            ),
        ],
        "Python": [
            st.Page(
                "views/python_exercises.py",
                title="Exercices Python",
                icon="🐍",
                url_path="python",
            ),
            st.Page(
                "views/python_flashcards.py",
                title="Mémocards Python",
                icon="🃏",
                url_path="python-memocards",
            ),
        ],
    }
)

collapse_sidebar_on_mobile()
navigation.run()
