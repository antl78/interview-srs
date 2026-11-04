"""Comportement du runner dans un vrai processus séparé : bonne réponse,
mauvaise réponse, erreurs, délai dépassé, print parasites."""

from pathlib import Path

import pytest

from python_check import run_tests
from python_runner import compare

EXERCISES = Path(__file__).resolve().parent.parent / "python_exercises" / "basics"
REVERSE = EXERCISES / "01_reverse_words.py"
SECOND = EXERCISES / "02_second_largest.py"


def test_correct_answer_passes():
    out = run_tests(REVERSE, "def reverse_words(s):\n    return ' '.join(reversed(s.split()))\n")
    assert out["status"] == "ok"
    assert all(r["passed"] for r in out["results"])


def test_wrong_answer_fails_some_cases():
    out = run_tests(REVERSE, "def reverse_words(s):\n    return s[::-1]\n")
    assert out["status"] == "ok"
    assert not all(r["passed"] for r in out["results"])


def test_missing_exception_is_reported():
    code = "def second_largest(n):\n    return sorted(set(n))[-2] if len(set(n)) > 1 else None\n"
    out = run_tests(SECOND, code)
    failed = [r for r in out["results"] if not r["passed"]]
    assert failed and all("pas d'exception" in r["got"] for r in failed)


def test_syntax_error():
    out = run_tests(REVERSE, "def reverse_words(s)\n    return s\n")
    assert out["status"] == "error" and "SyntaxError" in out["message"]


def test_missing_function():
    out = run_tests(REVERSE, "def other(s):\n    return s\n")
    assert out["status"] == "error" and "reverse_words" in out["message"]


def test_infinite_loop_times_out():
    out = run_tests(REVERSE, "def reverse_words(s):\n    while True:\n        pass\n", timeout=2)
    assert out["status"] == "timeout"


def test_prints_do_not_break_result():
    code = "print('top level')\ndef reverse_words(s):\n    print('debug', s)\n    return ' '.join(s.split()[::-1])\n"
    out = run_tests(REVERSE, code)
    assert out["status"] == "ok"
    assert out["results"][0]["stdout"].startswith("debug")


def test_input_mutation_does_not_leak():
    code = "def second_largest(n):\n    n.clear()\n    return 0\n"
    out = run_tests(SECOND, code)
    assert out["results"][0]["call"] == "second_largest([3, 1, 4, 1, 5])"


@pytest.mark.parametrize("got, expected, mode, ok", [
    ([1, 2], [1, 2], "exact", True),
    ((1, 2), [1, 2], "exact", False),      # tuple au lieu de list
    (True, 1, "exact", False),             # bool au lieu de int
    ([2, 1], [1, 2], "unordered", True),
    ([1, 1, 2], [1, 2], "unordered", False),
    (0.1 + 0.2, 0.3, "approx", True),
    ([0.1 + 0.2, 1], [0.3, 1.0], "approx", True),
])
def test_compare_modes(got, expected, mode, ok):
    assert compare(got, expected, mode)[0] is ok


def test_non_ascii_code_and_output():
    code = "def reverse_words(s):\n    print('déjà vu')\n    return ' '.join(s.split()[::-1])\n"
    out = run_tests(REVERSE, code)
    assert out["results"][0]["stdout"].startswith("déjà vu")
