META = {
    "title": "Is Leap Year",
    "function": "is_leap_year",
    "prompt": (
        "Renvoie `True` si `year` est une année bissextile, `False` sinon. "
        "Une année est bissextile si elle est divisible par 4, sauf les années "
        "divisibles par 100, qui ne le sont que si elles sont aussi divisibles par 400."
    ),
    "hints": [
        "Commence par le cas le plus restrictif : divisible par 400.",
        "1900 n'est pas bissextile, 2000 l'est.",
    ],
}


def is_leap_year(year: int) -> bool:
    """Reference solution."""
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


TEST_CASES = [
    {"args": (2024,), "expected": True},
    {"args": (2023,), "expected": False},
    {"args": (1900,), "expected": False, "note": "divisible par 100 mais pas par 400"},
    {"args": (2000,), "expected": True, "note": "divisible par 400"},
    {"args": (2100,), "expected": False, "note": "divisible par 100 mais pas par 400"},
    {"args": (1600,), "expected": True, "note": "divisible par 400"},
]
