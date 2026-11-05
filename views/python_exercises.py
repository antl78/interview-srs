"""Page Exercices Python : écrire une fonction dans l'éditeur, la vérifier
sur les cas de test de l'exercice, puis planifier la prochaine révision
(répétition espacée, track 'python')."""

from pathlib import Path

import pandas as pd
import streamlit as st
from code_editor import code_editor

from python_catalog import EXERCISES_DIR, load_catalog, load_exercise
from python_check import run_tests
from python_runner import format_call
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

# Matière de ces exercices dans la base de progression (colonne track).
TRACK = "python"

con = get_connection()


def exercise_files_signature() -> tuple:
    """(chemin, date de modification) de chaque fichier d'exercice : sert de
    clé au cache du catalogue, qui se recharge dès qu'un fichier change."""
    return tuple(
        (str(p), p.stat().st_mtime) for p in sorted(EXERCISES_DIR.rglob("*.py"))
    )


@st.cache_data
def get_catalog(signature: tuple) -> pd.DataFrame:
    return load_catalog()


def theme_levels(catalog: pd.DataFrame) -> dict:
    """{libellé de niveau : [thèmes]} pour theme_menu, dans l'ordre du
    catalogue (niveaux croissants, hors-séries à la fin)."""
    levels: dict[str, list[str]] = {}
    for row in catalog.drop_duplicates("theme").itertuples():
        prefix = "Hors-série" if pd.isna(row.level) else f"Niveau {int(row.level)}"
        levels.setdefault(f"{prefix} · {row.theme_label}", []).append(row.theme)
    return levels


# Bouton affiché DANS l'éditeur : le code n'est envoyé à Streamlit qu'au
# clic (ou Ctrl+Entrée), pas à chaque frappe. Un éditeur qui relance l'app
# à chaque touche (streamlit-ace en auto_update) perd des caractères.
EDITOR_BUTTONS = [
    {
        "name": "Valider",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "alwaysOn": True,  # sinon visible seulement au survol (absent sur mobile)
        "commands": ["submit"],
        "style": {
            "bottom": "0.44rem",
            "right": "0.4rem",
            # Vert du thème (.streamlit/config.toml) : bouton bien visible.
            "color": "white",
            "backgroundColor": "#22c55e",
            "borderRadius": "0.5rem",
            "opacity": 1,
        },
    }
]


def check_python_answer(code: str, exercise_path: str) -> None:
    """Lance les tests et range le verdict dans session_state (même
    mécanique que la page SQL)."""
    if not code.strip():
        st.session_state["check_result"] = {"status": "empty"}
        return
    outcome = run_tests(exercise_path, code)
    if outcome["status"] == "ok":
        outcome["correct"] = all(r["passed"] for r in outcome["results"])
    st.session_state["check_result"] = outcome
    st.session_state["last_check_correct"] = outcome.get("correct", False)


catalog = get_catalog(exercise_files_signature())

# Catalogue (fichiers) + progression (DuckDB). Le catalogue est enregistré
# comme vue DuckDB pour réutiliser la même logique de file que le SQL :
# un exercice sans ligne de progression est dû immédiatement.
con.register(
    "python_catalog",
    catalog[["exercise_name", "theme", "position", "level"]],
)
EXERCISE_STATE_CTE = """
WITH exercise_state AS (
    SELECT
        c.*,
        COALESCE(p.last_reviewed, DATE '1970-01-01') AS last_reviewed,
        COALESCE(p.interval_step, 0) AS interval_step
    FROM python_catalog AS c
    LEFT JOIN progress.exercise_progress AS p
        ON p.track = 'python'  -- = TRACK
        AND p.exercise_name = c.exercise_name
)
"""

with st.sidebar:
    due_df = con.execute(
        EXERCISE_STATE_CTE
        + "SELECT theme, "
        "COUNT(*) FILTER (WHERE last_reviewed <= CURRENT_DATE) AS due "
        "FROM exercise_state GROUP BY theme"
    ).df()
    due_by_theme = dict(zip(due_df["theme"], due_df["due"].astype(int)))
    st.metric("À réviser aujourd'hui", sum(due_by_theme.values()))

    st.markdown("**Que voulez-vous revoir ?**")
    theme = theme_menu(
        catalog["theme"].drop_duplicates().tolist(),
        theme_levels(catalog),
        "selected_python_theme",
        counts=due_by_theme,
    )

if catalog.empty:
    st.info("Aucun exercice Python pour l'instant.")
elif not theme:
    st.info("Sélectionnez un thème dans la barre à gauche")
else:
    exercise_name, interval_step = con.execute(
        EXERCISE_STATE_CTE
        + "SELECT exercise_name, interval_step FROM exercise_state "
        "WHERE theme = ? ORDER BY last_reviewed, position LIMIT 1",
        [theme],
    ).fetchone()
    entry = catalog[catalog["exercise_name"] == exercise_name].iloc[0]
    exercise = load_exercise(Path(entry["path"]))

    # Changement d'exercice : verdict effacé, éditeur neuf, retour en haut.
    # Préfixe "python:" : un exercice SQL du même nom ne doit pas garder
    # le verdict en passant d'une page à l'autre.
    checked_key = f"{TRACK}:{exercise_name}"
    if st.session_state.get("checked_exercise") != checked_key:
        st.session_state["last_check_correct"] = None
        st.session_state["check_result"] = None
        st.session_state["checked_exercise"] = checked_key
        scroll_to_top(checked_key)

    st.subheader(entry["title"])
    level_label = (
        "Hors-série" if pd.isna(entry["level"]) else f"Niveau {int(entry['level'])}"
    )
    st.caption(f"{level_label} · {entry['theme_label']}")
    st.markdown(entry["prompt"])

    # Exemples = cas de test sans note (les cas limites, annotés, restent
    # à découvrir, comme en entretien).
    examples = [c for c in exercise["test_cases"] if not c.get("note")]
    if examples:
        st.code(
            "\n".join(
                f"{format_call(entry['function_name'], c)}  # → "
                + (c["raises"].__name__ if "raises" in c else repr(c["expected"]))
                for c in examples
            ),
            language="python",
        )

    # Clé dépendante de l'exercice : éditeur neuf, pré-rempli avec la
    # signature, à chaque changement d'exercice.
    response = code_editor(
        entry["starter_code"],
        lang="python",
        height=[8, 25],  # nombre de lignes min / max (grandit avec le code)
        buttons=EDITOR_BUTTONS,
        options={
            "wrap": True,  # pas de défilement horizontal sur mobile
            "tabSize": 4,
            "showPrintMargin": False,
            # Autocomplétion coupée : sa liste de suggestions capture la
            # touche Entrée (Entrée après "def f():" insérait "self"), et
            # en entretien on code sans elle.
            "enableLiveAutocompletion": False,
            "enableBasicAutocompletion": False,
            "enableSnippets": False,
        },
        key=f"python_editor_{exercise_name}",
    )
    st.caption("Sur PC : Ctrl+Entrée pour valider.")

    # Chaque clic sur Valider renvoie un id neuf : on ne lance les tests
    # qu'une fois par soumission, pas à chaque rerun de la page.
    if response["type"] == "submit" and response["id"] != st.session_state.get(
        "python_last_submission"
    ):
        st.session_state["python_last_submission"] = response["id"]
        with st.spinner("Exécution des tests…"):
            check_python_answer(response["text"], entry["path"])

    # Verdict et bouton de suite AVANT le détail (cf. ergonomie mobile).
    check_result = st.session_state.get("check_result")
    if check_result:
        status = check_result["status"]
        if status == "empty":
            st.warning("Écrivez votre fonction avant de valider.")
        elif status in ("error", "timeout"):
            st.error("Votre code n'a pas pu être exécuté :")
            st.code(check_result["message"], language="text")
        else:
            results = check_result["results"]
            nb_passed = sum(r["passed"] for r in results)
            if check_result["correct"]:
                st.success(f"✅ Tous les tests passent ({nb_passed}/{len(results)})")
            else:
                st.error(
                    f"❌ {nb_passed} test{'s' if nb_passed > 1 else ''} sur "
                    f"{len(results)} réussi{'s' if nb_passed > 1 else ''}"
                )

    if st.session_state.get("last_check_correct") is True:
        next_days, new_step = next_review(int(interval_step))
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
            "son intervalle à 2 jours."
        ),
        on_click=reset_exercise_now,
        args=(TRACK, exercise_name),
    )

    if check_result and check_result["status"] == "ok":
        with st.expander("Détail des tests", expanded=not check_result["correct"]):
            st.dataframe(
                pd.DataFrame([
                    {
                        "": "✅" if r["passed"] else "❌",
                        "Appel": r["call"],
                        "Attendu": r["expected"],
                        "Obtenu": r["got"],
                        "Cas": r["note"],
                    }
                    for r in check_result["results"]
                ]),
                hide_index=True,
            )
            for r in check_result["results"]:
                if r.get("error") or r["stdout"]:
                    st.caption(r["call"])
                    st.code((r["stdout"] or "") + (r.get("error") or ""), language="text")

    tab_hints, tab_solution = st.tabs(["Indices", "Solution"])
    with tab_hints:
        hints = entry["hints"]
        if not hints:
            st.caption("Pas d'indice pour cet exercice.")
        for i, hint in enumerate(hints, start=1):
            with st.expander(f"Indice {i}"):
                st.markdown(hint)
    with tab_solution:
        st.code(exercise["reference_source"], language="python")
