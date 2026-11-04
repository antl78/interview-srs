"""Garde-fous du contenu Python : chaque exercice respecte le format, et
sa solution de référence passe tous ses cas de test.
Lancer : uv run pytest"""

from pathlib import Path

import pytest

from python_catalog import load_catalog, load_exercise
from python_runner import evaluate

CATALOG = load_catalog()


def test_catalog_is_not_empty():
    assert not CATALOG.empty


@pytest.mark.parametrize("path", CATALOG["path"], ids=CATALOG["exercise_name"])
def test_reference_solution_passes_all_cases(path):
    exercise = load_exercise(Path(path))
    results = evaluate(exercise["function"], exercise["test_cases"])
    failures = [r for r in results if not r["passed"]]
    assert not failures, failures


@pytest.mark.parametrize("path", CATALOG["path"], ids=CATALOG["exercise_name"])
def test_has_edge_case(path):
    """Au moins un cas annoté (note) : les cas limites sont obligatoires."""
    exercise = load_exercise(Path(path))
    assert any(case.get("note") for case in exercise["test_cases"])
