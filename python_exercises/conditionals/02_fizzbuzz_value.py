META = {
    "title": "FizzBuzz Value",
    "function": "fizzbuzz_value",
    "prompt": (
        "Renvoie `\"FizzBuzz\"` si `n` est divisible par 3 et par 5, `\"Fizz\"` "
        "s'il est divisible par 3 seulement, `\"Buzz\"` s'il est divisible par 5 "
        "seulement, et sinon `n` converti en chaîne (`7` → `\"7\"`)."
    ),
    "hints": [
        "`n % 3 == 0` teste si `n` est divisible par 3.",
        "L'ordre des conditions compte : le cas le plus précis doit être testé en premier.",
    ],
}


def fizzbuzz_value(n: int) -> str:
    """Reference solution."""
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


TEST_CASES = [
    {"args": (3,), "expected": "Fizz"},
    {"args": (10,), "expected": "Buzz"},
    {"args": (7,), "expected": "7", "note": "renvoie une chaîne, pas un entier"},
    {"args": (15,), "expected": "FizzBuzz", "note": "divisible par 3 et par 5"},
    {"args": (45,), "expected": "FizzBuzz", "note": "multiple de 15"},
    {"args": (1,), "expected": "1"},
]
