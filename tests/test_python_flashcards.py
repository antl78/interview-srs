"""Garde-fous des mémocards Python : format valide, noms uniques, et chaque
exemple s'exécute en affichant exactement la sortie annoncée.
Lancer : uv run pytest"""

import pytest

from python_flashcard_catalog import FlashcardFormatError, load_flashcards, run_example

CARDS = load_flashcards()


def test_flashcards_are_not_empty():
    assert not CARDS.empty


@pytest.mark.parametrize("card", CARDS.to_dict("records"), ids=CARDS["card_name"])
def test_example_prints_expected_output(card):
    printed = run_example(card["example"])
    if card["output"] is not None:
        assert printed.rstrip("\n") == card["output"].rstrip("\n")


def write(tmp_path, name, body):
    (tmp_path / name).write_text(body, encoding="utf-8")


def test_duplicate_card_name_is_rejected(tmp_path):
    card = '{"name": "dup", "question": "q", "answer": "a", "example": "pass"}'
    for theme in ("first", "second"):
        write(tmp_path, f"{theme}.py", f'THEME = {{"level": 2, "label": "x"}}\nCARDS = [{card}]\n')
    with pytest.raises(FlashcardFormatError, match="déjà définie"):
        load_flashcards(tmp_path)


def test_missing_key_is_rejected(tmp_path):
    write(tmp_path, "theme.py", 'THEME = {"level": 2, "label": "x"}\nCARDS = [{"name": "a", "question": "q"}]\n')
    with pytest.raises(FlashcardFormatError, match="clés requises"):
        load_flashcards(tmp_path)


def test_unknown_key_is_rejected(tmp_path):
    card = '{"name": "a", "question": "q", "answer": "a", "example": "pass", "ouput": "x"}'
    write(tmp_path, "theme.py", f'THEME = {{"level": 2, "label": "x"}}\nCARDS = [{card}]\n')
    with pytest.raises(FlashcardFormatError, match="clés inconnues"):
        load_flashcards(tmp_path)
