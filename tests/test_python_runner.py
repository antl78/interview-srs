"""Comportement du runner dans un vrai processus séparé : bonne réponse,
mauvaise réponse, erreurs, délai dépassé, print parasites."""

from pathlib import Path

import pytest

from python_check import run_tests
from python_runner import compare, format_call, run_case

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


def take_3(gen):
    return [next(gen) for _ in range(3)]


def call_with_10(func, *args):
    return func(10)


def test_then_consumes_result():
    def naturals():
        n = 0
        while True:
            yield n
            n += 1

    case = {"args": (), "then": take_3, "expected": [0, 1, 2]}
    result = run_case(naturals, case)
    assert result["passed"]
    assert result["call"] == "take_3(naturals())"


def test_then_receives_args_and_shows_function_names():
    def double(x):
        return 2 * x

    def identity_decorator(func):
        return func

    case = {"args": (double,), "then": call_with_10, "expected": 20}
    result = run_case(identity_decorator, case)
    assert result["passed"]
    assert result["call"] == "call_with_10(identity_decorator(double))"


def test_then_exception_is_reported():
    def not_a_generator():
        return 42

    case = {"args": (), "then": take_3, "expected": [0, 1, 2]}
    result = run_case(not_a_generator, case)
    assert not result["passed"] and result["got"].startswith("TypeError")


def test_then_with_raises():
    def make_failing():
        def inner(x):
            raise ValueError("boom")
        return inner

    case = {"args": (), "then": call_with_10, "raises": ValueError}
    assert run_case(make_failing, case)["passed"]
