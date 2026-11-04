"""Page Exercices SQL : écrire une requête, la comparer à la solution,
puis planifier la prochaine révision (répétition espacée)."""

import streamlit as st

from sql_check import run_check, run_dml_in_sandbox
from srs_core import (
    REVIEW_INTERVALS,
    advance_exercise,
    get_connection,
    next_review,
    reschedule_exercise,
    reset_exercise_now,
    scroll_to_top,
    theme_menu,
)

con = get_connection()

# Matière de ces exercices dans la base de progression (colonne track).
TRACK = "sql"

# Exercices + état de révision. Un exercice sans ligne dans
# exercise_progress n'a jamais été révisé : il est dû immédiatement.
# position (rowid) départage les ex aequo dans l'ordre du programme.
EXERCISE_STATE_CTE = """
WITH exercise_state AS (
    SELECT
        e.*,
        e.rowid AS position,
        COALESCE(p.last_reviewed, DATE '1970-01-01') AS last_reviewed,
        COALESCE(p.interval_step, 0) AS interval_step
    FROM exercises AS e
    LEFT JOIN progress.exercise_progress AS p
        ON p.track = 'sql'  -- = TRACK
        AND p.exercise_name = e.exercise_name
)
"""

# Thèmes par niveau de maîtrise SQL (cf. doc du projet), dans l'ordre
# d'affichage de la barre latérale. Un thème absent de ces dictionnaires
# est affiché dans un groupe "Autres", à la fin.
EXERCISE_THEME_LEVELS = {
    "Niveau 2 · Joins, CTE, CRUD": [
        "cross_joins", "inner_joins", "left_joins", "outer_join",
        "self_joins", "cte", "crud",
    ],
    "Niveau 3 · Agrégations, CASE WHEN, GROUPING SETS": [
        "aggregation", "case_when", "grouping_sets",
    ],
    "Niveau 4 · Agrégations conditionnelles, dates": [
        "conditional_aggregation", "dates",
    ],
    "Niveau 5 · Window functions": [
        "window_functions", "ranking", "lag_lead",
    ],
}

with st.sidebar:
    theme_counts_df = con.execute(
        EXERCISE_STATE_CTE
        + "SELECT theme, "
        "COUNT(*) FILTER (WHERE last_reviewed <= CURRENT_DATE) AS due "
        "FROM exercise_state GROUP BY theme ORDER BY theme"
    ).df()
    due_by_theme = dict(zip(theme_counts_df["theme"], theme_counts_df["due"].astype(int)))
    st.metric("À réviser aujourd'hui", sum(due_by_theme.values()))

    st.markdown("**Que voulez-vous revoir ?**")
    theme = theme_menu(
        theme_counts_df["theme"].tolist(),
        EXERCISE_THEME_LEVELS,
        "selected_theme",
        counts=due_by_theme,
    )

    if theme:
        exercise = (
            con.execute(
                EXERCISE_STATE_CTE
                + "SELECT * FROM exercise_state WHERE theme = ? "
                "ORDER BY last_reviewed, position",
                [theme],
            )
            .df()
        )
        exercise_name = exercise.loc[0, "exercise_name"]
        st.caption(f"Exercice : {exercise_name.replace('_', ' ').title()}")

        with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
            answer = f.read()

        # Thème "crud" : la première table de l'exercice est celle dont
        # l'état final (après la requête) est comparé.
        check_table = (
            str(exercise.loc[0, "tables"][0]) if theme == "crud" else None
        )
        if check_table:
            solution_df = run_dml_in_sandbox(answer, check_table)
        else:
            solution_df = con.execute(answer).df()

if not theme:
    st.info("Sélectionnez un thème dans la barre à gauche")
else:
    # Un changement d'exercice (nouveau choix de thème, ou passage
    # automatique au suivant du même thème) efface le verdict précédent,
    # vide la zone de texte et remonte en haut de la page.
    if st.session_state.get("checked_exercise") != exercise_name:
        st.session_state["last_check_correct"] = None
        st.session_state["check_result"] = None
        st.session_state["checked_exercise"] = exercise_name
        scroll_to_top(exercise_name)

    st.subheader(exercise_name.replace("_", " ").title())
    st.write(exercise.loc[0, "statement"])

    # La clé dépend de l'exercice : Streamlit traite alors la zone de texte
    # comme un widget neuf à chaque changement d'exercice, donc vide par
    # défaut — plus fiable qu'essayer d'effacer une clé fixe après coup.
    text_key = f"user_input_{exercise_name}"
    st.text_area(
        label="Votre code SQL",
        help="Sur PC : Ctrl+Entrée pour valider.",
        key=text_key,
        on_change=run_check,
        args=(text_key, solution_df, check_table),
    )

    st.button(
        "Valider",
        type="primary",
        on_click=run_check,
        args=(text_key, solution_df, check_table),
    )

    # Verdict et bouton de suite AVANT le tableau de résultat : sur
    # mobile, un tableau de quelques lignes suffit à les pousser hors
    # de l'écran.
    check_result = st.session_state.get("check_result")
    if check_result:
        if check_result["status"] == "empty":
            st.warning("Veuillez entrer une requête SQL.")
        elif check_result["status"] == "error":
            st.error(f"Erreur SQL : {check_result['message']}")
        elif check_result["status"] == "ok":
            if check_result["correct"]:
                st.success("✅ Bonne réponse !")
                if check_result.get("renamed"):
                    st.caption(
                        "ℹ️ Les noms de colonnes diffèrent de la solution "
                        "(alias) — accepté, seules les valeurs comptent."
                    )
            else:
                st.error("❌ Ce n'est pas (encore) la bonne réponse.")

    interval_step = int(exercise.loc[0, "interval_step"])

    if st.session_state.get("last_check_correct") is True:
        next_days, new_step = next_review(interval_step)
        st.button(
            f"✅ Continuer → prochaine révision dans {next_days} jours",
            type="primary",
            on_click=advance_exercise,
            args=(TRACK, exercise_name, next_days, new_step),
        )
    elif st.session_state.get("last_check_correct") is False:
        st.button(
            f"🔁 Revoir dans {REVIEW_INTERVALS[0]} jours",
            on_click=reschedule_exercise,
            args=(TRACK, exercise_name, REVIEW_INTERVALS[0], 0),
        )

    st.button(
        "🔄 Remettre à réviser maintenant",
        help=(
            "Repasse cet exercice en tête de file dès aujourd'hui et remet "
            "son intervalle à 2 jours — utile pour le refaire tout de "
            "suite sans attendre son échéance normale."
        ),
        on_click=reset_exercise_now,
        args=(TRACK, exercise_name),
    )

    if check_result and check_result["status"] == "ok":
        with st.expander("Résultat de votre requête", expanded=True):
            if check_table:
                st.caption(
                    f"Table {check_table} après votre requête (modifications "
                    "annulées ensuite, la base n'est pas changée) :"
                )
            st.dataframe(check_result["result"], hide_index=True)

    tab2, tab3 = st.tabs(["Tables", "Solution"])

    with tab2:
        exercise_tables = exercise.loc[0, "tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table, hide_index=True)

    with tab3:
        st.code(answer, language="sql")
        st.caption(
            f"Table {check_table} après la solution :"
            if check_table
            else "Résultat de la solution :"
        )
        st.dataframe(solution_df, hide_index=True)
