"""Vérification des réponses SQL : exécution sécurisée de la requête de
l'utilisateur et comparaison de son résultat à celui de la solution."""

import itertools
from collections import Counter, defaultdict

import duckdb
import numpy as np
import pandas as pd
import streamlit as st

from srs_core import get_connection

# Claviers mobiles (iOS, Gboard) : la ponctuation "intelligente" remplace
# les guillemets droits par des guillemets typographiques, ce qui casse les
# littéraux SQL ('Alice' devient ’Alice’).
MOBILE_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})

# Garde-fou : nombre max de permutations testées quand plusieurs colonnes
# ont exactement les mêmes valeurs (cas rare, mais combinatoire).
MAX_COLUMN_PERMUTATIONS = 5000

# Instructions acceptées pour les exercices du thème "crud".
DML_STATEMENT_TYPES = {
    duckdb.StatementType.INSERT,
    duckdb.StatementType.UPDATE,
    duckdb.StatementType.DELETE,
}


def normalize_mobile_quotes(query_text: str) -> str:
    """Remplace les guillemets typographiques par des guillemets droits."""
    return query_text.translate(MOBILE_QUOTES)


def _normalize_value(v):
    """1 et 1.0 doivent être considérés comme égaux : on normalise les
    nombres flottants entiers vers leur écriture entière avant comparaison."""
    if v is None or (pd.api.types.is_scalar(v) and pd.isna(v)):
        return "NULL"
    if isinstance(v, (float, np.floating)):
        if float(v).is_integer():
            return str(int(v))
        return repr(round(float(v), 9))
    return str(v)


def dataframes_match(user_df: pd.DataFrame, solution_df: pd.DataFrame) -> bool:
    """Compare deux résultats de requête sur leurs VALEURS uniquement :
    - noms de colonnes ignorés (un alias différent reste une bonne réponse) ;
    - ordre des colonnes et des lignes indifférent ;
    - int vs float (1 vs 1.0) indifférent.

    Les colonnes sont appariées par leur contenu (multiset de valeurs), puis
    les lignes sont comparées en multiset. Si plusieurs colonnes ont le même
    contenu, on essaie les appariements possibles entre elles."""
    if user_df.shape != solution_df.shape:
        return False

    # Colonnes renommées en positions : évite les soucis de noms dupliqués
    # (ex : SELECT * avec JOIN ... ON qui renvoie order_id et order_id_1).
    user = user_df.map(_normalize_value)
    solution = solution_df.map(_normalize_value)
    user.columns = range(user.shape[1])
    solution.columns = range(solution.shape[1])

    def signature(col: pd.Series) -> tuple:
        return tuple(sorted(col))

    user_groups: dict = defaultdict(list)
    for c in user.columns:
        user_groups[signature(user[c])].append(c)
    solution_groups: dict = defaultdict(list)
    for c in solution.columns:
        solution_groups[signature(solution[c])].append(c)

    if {k: len(v) for k, v in user_groups.items()} != {
        k: len(v) for k, v in solution_groups.items()
    }:
        return False

    solution_rows = Counter(map(tuple, solution.to_numpy().tolist()))
    sigs = list(solution_groups)
    candidate_orders = itertools.product(
        *(itertools.permutations(user_groups[s]) for s in sigs)
    )
    for combo in itertools.islice(candidate_orders, MAX_COLUMN_PERMUTATIONS):
        mapping = {}
        for s, user_cols in zip(sigs, combo):
            mapping.update(zip(solution_groups[s], user_cols))
        reordered = user[[mapping[c] for c in solution.columns]]
        if Counter(map(tuple, reordered.to_numpy().tolist())) == solution_rows:
            return True
    return False


def run_dml_in_sandbox(query_text: str, check_table: str) -> pd.DataFrame:
    """Exécute des INSERT/UPDATE/DELETE dans une transaction, lit l'état de
    check_table, puis annule tout (ROLLBACK) : la base n'est jamais modifiée,
    un exercice CRUD peut donc être refait à l'identique.

    cursor() ouvre une connexion séparée sur la même base, avec sa propre
    transaction : la connexion partagée (cache_resource) et les autres
    sessions ne voient jamais les modifications en cours."""
    cursor = get_connection().cursor()
    try:
        cursor.begin()
        cursor.execute(query_text)
        # check_table vient de exercises (jamais de la saisie
        # utilisateur) ; on le quote quand même comme identifiant.
        quoted_table = '"' + check_table.replace('"', '""') + '"'
        return cursor.execute(f"SELECT * FROM {quoted_table}").df()
    finally:
        cursor.rollback()
        cursor.close()


def _set_error(message: str) -> None:
    st.session_state["check_result"] = {"status": "error", "message": message}
    st.session_state["last_check_correct"] = False


def run_check(
    text_key: str, solution_df: pd.DataFrame, check_table: str | None = None
) -> None:
    """Exécute la requête et range le verdict dans session_state, sans
    appeler directement st.write/st.dataframe/... : cette fonction sert
    de callback (Ctrl+Entrée et bouton Valider), et Streamlit déconseille
    d'afficher des éléments depuis un callback.

    check_table renseigné = exercice CRUD : la requête est exécutée en
    bac à sable (run_dml_in_sandbox) et c'est l'état final de cette table
    qui est comparé à la solution."""
    query_text = normalize_mobile_quotes(st.session_state.get(text_key, ""))
    if not query_text.strip():
        st.session_state["check_result"] = {"status": "empty"}
        return

    con = get_connection()
    try:
        statements = con.extract_statements(query_text)
        if check_table:
            # Exercice CRUD : une ou plusieurs instructions INSERT / UPDATE /
            # DELETE (CTE autorisées), rien d'autre (pas de DROP, CREATE,
            # BEGIN/COMMIT...).
            if not statements or any(
                s.type not in DML_STATEMENT_TYPES for s in statements
            ):
                _set_error(
                    "Exercice CRUD : seules des instructions INSERT, "
                    "UPDATE ou DELETE sont acceptées."
                )
                return
            result = run_dml_in_sandbox(query_text, check_table)
        else:
            # La connexion est en lecture/écriture (bac à sable CRUD,
            # base de progression attachée) : on n'accepte qu'UNE
            # instruction de type SELECT (CTE incluses), sinon un
            # DROP/DELETE/UPDATE tapé dans la zone de texte modifierait
            # réellement la base.
            if len(statements) != 1 or statements[0].type != duckdb.StatementType.SELECT:
                _set_error(
                    "Seule une requête SELECT (une seule instruction, "
                    "CTE autorisées) est acceptée."
                )
                return
            result = con.execute(query_text).df()
    except Exception as e:  # pylint: disable=broad-exception-caught
        _set_error(str(e))
        return

    correct = dataframes_match(result, solution_df)
    renamed = correct and sorted(map(str, result.columns)) != sorted(
        map(str, solution_df.columns)
    )
    st.session_state["check_result"] = {
        "status": "ok",
        "result": result,
        "correct": correct,
        "renamed": renamed,
    }
    st.session_state["last_check_correct"] = correct
