META = {
    "title": "Digit Sum",
    "function": "digit_sum",
    "prompt": (
        "Renvoie la somme des chiffres de l'entier positif ou nul `n` "
        "(`472` → `4 + 7 + 2 = 13`), avec une boucle `while`."
    ),
    "hints": [
        "`n % 10` donne le dernier chiffre, `n // 10` le retire.",
        "Boucle tant que `n > 0`.",
    ],
}


def digit_sum(n: int) -> int:
    """Reference solution."""
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total


TEST_CASES = [
    {"args": (472,), "expected": 13},
    {"args": (9999,), "expected": 36},
    {"args": (1000,), "expected": 1, "note": "zéros au milieu et à la fin"},
    {"args": (7,), "expected": 7, "note": "un seul chiffre"},
    {"args": (0,), "expected": 0, "note": "zéro"},
]
