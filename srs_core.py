"""Socle commun de l'app de révision : connexion DuckDB, progression en
répétition espacée et éléments d'interface partagés entre les pages
(menu des thèmes, retour en haut, barre latérale sur mobile).

Rien ici n'est spécifique au SQL : une future page Python s'appuie sur les
mêmes fonctions."""

import logging
import os
from datetime import date, timedelta

import duckdb
import streamlit as st

CONTENT_DB = "data/exercises_sql_tables.duckdb"
PROGRESS_DB = "data/progress.duckdb"

# Colonnes de progression stockées dans la base de contenu avant la
# séparation contenu / progression (cf. migrate_legacy_progress).
LEGACY_PROGRESS_COLUMNS = ("last_reviewed", "interval_step")

REVIEW_INTERVALS = [2, 7, 21]  # jours, du plus court au plus long

# Largeur (px) sous laquelle on considère l'écran comme mobile : la barre
# latérale y recouvre la page, on la referme après le choix d'un thème.
MOBILE_MAX_WIDTH = 768


def ensure_content_db() -> None:
    """Crée la base de contenu via init_db.py si elle n'existe pas encore
    (premier lancement, ex : Streamlit Cloud). Exécuté dans un espace de
    noms séparé pour que les variables d'init_db.py (dont son propre
    `con`) n'écrasent rien ici."""
    if not os.path.isdir("data"):
        logging.debug("creating folder data")
        os.mkdir("data")
    if os.path.exists(CONTENT_DB):
        return
    namespace: dict = {"__name__": "__main__"}
    with open("init_db.py", encoding="utf-8") as f:
        exec(f.read(), namespace)  # pylint: disable=exec-used
    init_con = namespace.get("con")
    if init_con is not None:
        init_con.close()


def has_column(connection: duckdb.DuckDBPyConnection, table: str, column: str) -> bool:
    """True si la table de la base de contenu possède cette colonne."""
    return connection.execute(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_catalog = current_database() "
        "AND table_name = ? AND column_name = ?",
        [table, column],
    ).fetchone()[0] > 0


def migrate_legacy_progress(connection: duckdb.DuckDBPyConnection) -> None:
    """Migration unique d'une base créée avant la séparation contenu /
    progression : renomme memory_state en exercises, copie la progression
    existante vers progress.duckdb, puis retire les colonnes de progression
    de la base de contenu. Idempotente : ne fait rien sur une base à jour."""
    content_tables = {
        row[0]
        for row in connection.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_catalog = current_database()"
        ).fetchall()
    }
    if "memory_state" in content_tables and "exercises" not in content_tables:
        connection.execute("ALTER TABLE memory_state RENAME TO exercises")

    if has_column(connection, "exercises", "last_reviewed"):
        # Seuls les exercices déjà révisés sont copiés : les dates par
        # défaut (1970 / 1980) signifiaient "jamais révisé", ce qui
        # correspond désormais à l'absence de ligne dans exercise_progress.
        connection.execute("""
            INSERT INTO progress.exercise_progress
            SELECT exercise_name, CAST(last_reviewed AS DATE), interval_step
            FROM exercises
            WHERE CAST(last_reviewed AS DATE) > DATE '1980-01-01'
            ON CONFLICT DO NOTHING
        """)

    # Noms de colonnes constants (jamais issus d'une saisie utilisateur).
    for table in ("exercises", "flashcards"):
        for column in LEGACY_PROGRESS_COLUMNS:
            connection.execute(f"ALTER TABLE {table} DROP COLUMN IF EXISTS {column}")


@st.cache_resource
def get_connection() -> duckdb.DuckDBPyConnection:
    """Connexion DuckDB unique, réutilisée entre les reruns et les pages.

    Deux bases distinctes :
    - CONTENT_DB : exercices, tables d'exercices et mémocards. Versionnée dans
      le repo, régénérable par init_db.py ; l'app n'y écrit jamais (le bac à
      sable CRUD est annulé par ROLLBACK).
    - PROGRESS_DB : progression de révision, locale et ignorée par git,
      attachée sous le nom "progress" (créée au premier lancement)."""
    ensure_content_db()
    connection = duckdb.connect(database=CONTENT_DB, read_only=False)
    # Chemin constant : ATTACH n'accepte pas de paramètre préparé.
    connection.execute(f"ATTACH '{PROGRESS_DB}' AS progress")
    connection.execute("""
        CREATE TABLE IF NOT EXISTS progress.exercise_progress (
            exercise_name VARCHAR PRIMARY KEY,
            last_reviewed DATE NOT NULL,
            interval_step INTEGER NOT NULL
        )
    """)
    migrate_legacy_progress(connection)
    return connection


# --- Progression (répétition espacée) ---------------------------------------

def clear_verdict() -> None:
    """Efface le verdict de l'exercice en cours (après un changement de
    planification)."""
    st.session_state["last_check_correct"] = None
    st.session_state["check_result"] = None


def save_progress(name: str, days_from_today: int, interval_step: int) -> None:
    """Programme la prochaine révision d'un exercice (upsert dans la base
    de progression)."""
    get_connection().execute(
        "INSERT INTO progress.exercise_progress VALUES (?, ?, ?) "
        "ON CONFLICT (exercise_name) DO UPDATE SET "
        "last_reviewed = excluded.last_reviewed, "
        "interval_step = excluded.interval_step",
        [name, date.today() + timedelta(days=days_from_today), interval_step],
    )


def next_review(interval_step: int) -> tuple[int, int]:
    """(jours avant la prochaine révision, nouvel interval_step) après une
    bonne réponse."""
    next_days = REVIEW_INTERVALS[min(interval_step, len(REVIEW_INTERVALS) - 1)]
    new_step = min(interval_step + 1, len(REVIEW_INTERVALS) - 1)
    return next_days, new_step


def advance_exercise(name: str, next_days: int, new_step: int) -> None:
    """Callback (on_click) du bouton Continuer : programme la prochaine
    révision. Volontairement PAS de st.rerun() ici — un st.rerun() appelé
    depuis un gestionnaire de bouton a provoqué une perte aléatoire de la
    sélection de thème (session_state vidé) une fois sur deux ; un on_click
    s'exécute avant le script principal, qui repart de toute façon avec les
    données à jour au rerun naturel déclenché par le clic."""
    save_progress(name, next_days, new_step)
    clear_verdict()


def reschedule_exercise(name: str, days: int, step: int = 0) -> None:
    """Callback (on_click) du bouton Revoir plus tard."""
    save_progress(name, days, step)
    clear_verdict()


def reset_exercise_now(name: str) -> None:
    """Callback (on_click) du bouton Reset : sans ligne de progression,
    l'exercice redevient "jamais révisé", donc dû immédiatement."""
    get_connection().execute(
        "DELETE FROM progress.exercise_progress WHERE exercise_name = ?",
        [name],
    )
    clear_verdict()


# --- Interface partagée -------------------------------------------------------

def scroll_to_top(exercise_name: str) -> None:
    """Force le retour en haut de la page (utile en changeant d'exercice,
    Streamlit ne le fait pas tout seul après un st.rerun()).

    Désactive aussi l'autocorrection / la majuscule automatique du clavier
    mobile sur la zone de saisie. La zone de texte est recréée à chaque
    exercice (clé dépendante de l'exercice) et peut ne pas encore exister
    quand le script s'exécute : on réessaie quelques fois. exercise_name
    rend le contenu unique, sinon Streamlit ne réexécute pas le composant."""
    st.components.v1.html(
        f"<!-- {exercise_name} -->"
        "<script>"
        "var doc = window.parent.document;"
        "var m = doc.querySelector('[data-testid=\"stMain\"]');"
        "if (m) { m.scrollTo(0, 0); }"
        "var tries = 0;"
        "var timer = setInterval(function () {"
        "  doc.querySelectorAll('textarea').forEach(function (t) {"
        "    t.setAttribute('autocapitalize', 'off');"
        "    t.setAttribute('autocorrect', 'off');"
        "    t.setAttribute('autocomplete', 'off');"
        "    t.setAttribute('spellcheck', 'false');"
        "  });"
        "  if (++tries > 10) { clearInterval(timer); }"
        "}, 300);"
        "</script>",
        height=0,
    )


def collapse_sidebar_on_mobile() -> None:
    """Referme la barre latérale sur petit écran, une seule fois après un
    clic sur un thème (drapeau posé par select_theme). Sur PC, la barre
    latérale ne recouvre pas la page : elle reste ouverte."""
    if not st.session_state.pop("collapse_sidebar", False):
        return
    st.components.v1.html(
        # Compteur dans le contenu : force la réexécution du composant même
        # si l'on choisit deux fois de suite le même thème.
        f"<!-- {st.session_state.get('collapse_count', 0)} -->"
        # Le composant peut s'exécuter avant la fin du rendu de la page (il
        # est affiché avant elle) : on réessaie quelques fois, jusqu'à ce
        # que la barre soit bien repliée.
        "<script>"
        "var doc = window.parent.document;"
        "var tries = 0;"
        "var timer = setInterval(function () {"
        "  var sb = doc.querySelector('[data-testid=\"stSidebar\"]');"
        f"  if (window.parent.innerWidth >= {MOBILE_MAX_WIDTH} || ++tries > 10"
        "      || (sb && sb.getAttribute('aria-expanded') === 'false')) {"
        "    clearInterval(timer); return;"
        "  }"
        "  var b = doc.querySelector("
        "    '[data-testid=\"stSidebarCollapseButton\"] button');"
        "  if (b) { b.click(); }"
        "}, 250);"
        "</script>",
        height=0,
    )


def select_theme(state_key: str, theme_name: str) -> None:
    """Callback (on_click) d'un bouton de thème dans la barre latérale."""
    st.session_state[state_key] = theme_name
    st.session_state["collapse_sidebar"] = True
    st.session_state["collapse_count"] = st.session_state.get("collapse_count", 0) + 1


def theme_menu(
    themes: list,
    theme_levels: dict,
    state_key: str,
    counts: dict | None = None,
) -> str | None:
    """Affiche les thèmes dans la barre latérale, regroupés par niveau
    (séparateur + titre de niveau), et renvoie le thème sélectionné.

    Un st.radio ne permet pas d'insérer des séparateurs entre ses options :
    chaque thème est donc un bouton, et le thème choisi est gardé dans
    session_state[state_key] (clé non liée à un widget). counts (facultatif)
    ajoute un compteur au label : contrairement au format_func d'un radio,
    un label de bouton n'a pas de valeur persistée à perdre."""
    grouped_themes = [
        (level, [t for t in level_themes if t in themes])
        for level, level_themes in theme_levels.items()
    ]
    known_themes = {t for _, level_themes in grouped_themes for t in level_themes}
    other_themes = [t for t in themes if t not in known_themes]
    if other_themes:
        grouped_themes.append(("Autres", other_themes))

    for level, level_themes in grouped_themes:
        if not level_themes:
            continue
        st.divider()
        st.caption(level)
        for t in level_themes:
            label = t.replace("_", " ").title()
            count = (counts or {}).get(t, 0)
            st.button(
                f"{label} ({count})" if count else label,
                key=f"{state_key}_button_{t}",
                type="primary" if st.session_state.get(state_key) == t else "tertiary",
                width="stretch",
                on_click=select_theme,
                args=(state_key, t),
            )

    selected = st.session_state.get(state_key)
    return selected if selected in themes else None
