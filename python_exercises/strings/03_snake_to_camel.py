META = {
    "title": "Snake to camel",
    "function": "snake_to_camel",
    "prompt": (
        "Convertit `name`, écrit en snake_case minuscule, en camelCase : le "
        "premier mot reste tel quel, les suivants prennent une majuscule "
        "initiale. Les underscores en trop (multiples, au début, à la fin) "
        "sont ignorés."
    ),
    "hints": [
        "`split(\"_\")` puis `join`.",
        "`\"__a\".split(\"_\")` donne `['', '', 'a']` : filtre les morceaux vides.",
    ],
}


def snake_to_camel(name: str) -> str:
    """Reference solution."""
    words = [word for word in name.split("_") if word]
    if not words:
        return ""
    first, *rest = words
    return first + "".join(word.capitalize() for word in rest)


TEST_CASES = [
    {"args": ("user_id",), "expected": "userId"},
    {"args": ("get_http_response",), "expected": "getHttpResponse"},
    {"args": ("name",), "expected": "name", "note": "un seul mot"},
    {"args": ("__private_value",), "expected": "privateValue", "note": "underscores au début"},
    {"args": ("max__count_",), "expected": "maxCount", "note": "underscores multiples et final"},
    {"args": ("",), "expected": "", "note": "chaîne vide"},
]
