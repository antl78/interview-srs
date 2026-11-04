"""Exécution et vérification d'une réponse Python, dans un processus séparé.

Lancé par python_check.run_tests :
    python -I python_runner.py <fichier_exercice>   (code utilisateur sur stdin)
Écrit le résultat en JSON sur stdout, après la ligne RESULT_MARKER.

Volontairement autonome (aucun import du projet) : le mode isolé -I ne met
pas le dossier du projet dans sys.path. Les fonctions evaluate / compare
sont aussi importées directement par les tests pytest, pour vérifier que
chaque solution de référence passe ses propres cas de test.

Sécurité : le processus séparé protège l'app des boucles infinies (timeout)
et des plantages, PAS d'un code malveillant. Acceptable uniquement parce
que l'app est privée."""

import contextlib
import copy
import importlib.util
import io
import json
import math
import sys
import traceback
from collections import Counter

RESULT_MARKER = "__INTERVIEW_SRS_RESULT__"
MAX_REPR_LENGTH = 300
FLOAT_TOLERANCE = 1e-9


def short_repr(value) -> str:
    text = repr(value)
    return text if len(text) <= MAX_REPR_LENGTH else text[:MAX_REPR_LENGTH] + "…"


def format_call(function_name: str, case: dict) -> str:
    """Appel lisible, ex : top_k("a b", 2)"""
    parts = [short_repr(a) for a in case["args"]]
    parts += [f"{k}={short_repr(v)}" for k, v in case.get("kwargs", {}).items()]
    return f"{function_name}({', '.join(parts)})"


def approx_equal(got, expected) -> bool:
    """Égalité avec tolérance sur les flottants, récursive sur les
    list / tuple / dict. int et float sont interchangeables ici."""
    if isinstance(expected, bool) or isinstance(got, bool):
        return got is expected
    if isinstance(expected, (int, float)) and isinstance(got, (int, float)):
        return math.isclose(got, expected, rel_tol=FLOAT_TOLERANCE, abs_tol=FLOAT_TOLERANCE)
    if isinstance(expected, (list, tuple)):
        return (
            type(got) is type(expected)
            and len(got) == len(expected)
            and all(approx_equal(g, e) for g, e in zip(got, expected))
        )
    if isinstance(expected, dict):
        return (
            isinstance(got, dict)
            and got.keys() == expected.keys()
            and all(approx_equal(got[k], expected[k]) for k in expected)
        )
    return got == expected


def unordered_equal(got, expected) -> bool:
    """Mêmes éléments (doublons compris), ordre indifférent."""
    if type(got) is not type(expected):
        return False
    try:
        return Counter(got) == Counter(expected)
    except TypeError:  # éléments non hashables (ex : listes de listes)
        return sorted(got, key=repr) == sorted(expected, key=repr)


def compare(got, expected, mode: str = "exact") -> tuple[bool, str]:
    """(réussi, explication si échec). En mode exact, le type doit être
    exactement le même : renvoyer un tuple au lieu d'une liste, ou True
    au lieu de 1, est une erreur — c'est ce qu'attendrait un recruteur."""
    if mode == "approx":
        return approx_equal(got, expected), ""
    if mode == "unordered":
        return unordered_equal(got, expected), ""
    if mode != "exact":
        raise ValueError(f"mode de comparaison inconnu : {mode!r}")
    if type(got) is not type(expected):
        return False, f"type {type(got).__name__} au lieu de {type(expected).__name__}"
    return got == expected, ""


def run_case(function, case: dict) -> dict:
    """Exécute un cas de test. Les arguments sont copiés : une fonction qui
    modifie ses entrées ne fausse ni le cas suivant ni l'affichage."""
    args = copy.deepcopy(tuple(case["args"]))
    kwargs = copy.deepcopy(case.get("kwargs", {}))
    expected_exc = case.get("raises")
    result = {
        "call": format_call(function.__name__, case),
        "expected": (
            expected_exc.__name__ if expected_exc else short_repr(case["expected"])
        ),
        "note": case.get("note", ""),
    }
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            got = function(*args, **kwargs)
    except BaseException as exc:  # pylint: disable=broad-exception-caught
        if isinstance(exc, KeyboardInterrupt):
            raise
        if expected_exc and isinstance(exc, expected_exc):
            result.update(passed=True, got=type(exc).__name__)
        else:
            result.update(
                passed=False,
                got=f"{type(exc).__name__}: {exc}",
                error="".join(traceback.format_exception(exc)[-3:]),
            )
    else:
        if expected_exc:
            result.update(
                passed=False, got=f"{short_repr(got)} (pas d'exception levée)"
            )
        else:
            passed, reason = compare(got, case["expected"], case.get("compare", "exact"))
            result.update(
                passed=passed,
                got=short_repr(got) + (f" — {reason}" if reason else ""),
            )
    result["stdout"] = stdout.getvalue()[:2000]
    return result


def evaluate(function, test_cases: list) -> list[dict]:
    return [run_case(function, case) for case in test_cases]


def load_module(path: str):
    spec = importlib.util.spec_from_file_location("exercise_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    exercise = load_module(sys.argv[1])
    function_name = exercise.META["function"]
    # Octets décodés explicitement : sous Windows, stdin en pipe n'est pas
    # en UTF-8 par défaut (accents du code utilisateur mal lus).
    user_code = sys.stdin.buffer.read().decode("utf-8")

    namespace: dict = {"__name__": "user_solution"}
    output: dict
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(user_code, "<votre code>", "exec"), namespace)  # pylint: disable=exec-used
        function = namespace.get(function_name)
        if not callable(function):
            output = {
                "status": "error",
                "message": f"La fonction {function_name}() n'est pas définie.",
            }
        else:
            output = {"status": "ok", "results": evaluate(function, exercise.TEST_CASES)}
    except BaseException as exc:  # pylint: disable=broad-exception-caught
        if isinstance(exc, KeyboardInterrupt):
            raise
        output = {
            "status": "error",
            "message": "".join(traceback.format_exception_only(exc)).strip(),
        }

    # json.dumps échappe les non-ASCII : sortie lisible quel que soit
    # l'encodage de la console (cp1252 sous Windows).
    sys.__stdout__.write("\n" + RESULT_MARKER + "\n" + json.dumps(output) + "\n")
    sys.__stdout__.flush()


if __name__ == "__main__":
    main()
