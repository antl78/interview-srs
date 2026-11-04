META = {
    "title": "Validate age",
    "function": "validate_age",
    "prompt": (
        "Renvoie `age` s'il est valide. Lève une `TypeError` si `age` n'est pas "
        "un entier (les booléens ne comptent pas comme des entiers), et une "
        "`ValueError` s'il n'est pas entre 0 et 150 inclus."
    ),
    "hints": [
        "`TypeError` : mauvais type ; `ValueError` : bon type, mauvaise valeur.",
        "`isinstance(True, int)` vaut `True` : `bool` hérite de `int`.",
    ],
}


def validate_age(age: object) -> int:
    """Reference solution."""
    if isinstance(age, bool) or not isinstance(age, int):
        raise TypeError(f"age must be an int, got {type(age).__name__}")
    if not 0 <= age <= 150:
        raise ValueError(f"age out of range: {age}")
    return age


TEST_CASES = [
    {"args": (30,), "expected": 30},
    {"args": (150,), "expected": 150, "note": "borne incluse"},
    {"args": (-1,), "raises": ValueError, "note": "négatif"},
    {"args": ("30",), "raises": TypeError, "note": "chaîne"},
    {"args": (30.0,), "raises": TypeError, "note": "flottant"},
    {"args": (True,), "raises": TypeError, "note": "booléen"},
]
