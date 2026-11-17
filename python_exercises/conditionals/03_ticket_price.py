META = {
    "title": "Ticket Price",
    "function": "ticket_price",
    "prompt": (
        "Renvoie le prix d'un billet selon l'âge `age` : gratuit (`0`) avant 4 ans, "
        "`8` de 4 à 17 ans, `10` à partir de 65 ans, et `14` sinon."
    ),
    "hints": [
        "Une chaîne de `if` / `elif` / `else`, une tranche d'âge par branche.",
        "Vérifie les bornes : 4 ans paie déjà, 17 ans est encore un tarif réduit, "
        "65 ans a droit au tarif senior.",
    ],
}


def ticket_price(age: int) -> int:
    """Reference solution."""
    if age < 4:
        return 0
    elif age < 18:
        return 8
    elif age >= 65:
        return 10
    else:
        return 14


TEST_CASES = [
    {"args": (30,), "expected": 14},
    {"args": (10,), "expected": 8},
    {"args": (70,), "expected": 10},
    {"args": (2,), "expected": 0},
    {"args": (4,), "expected": 8, "note": "borne : 4 ans"},
    {"args": (17,), "expected": 8, "note": "borne : 17 ans"},
    {"args": (18,), "expected": 14, "note": "borne : 18 ans"},
    {"args": (65,), "expected": 10, "note": "borne : 65 ans"},
    {"args": (0,), "expected": 0, "note": "nouveau-né"},
]
