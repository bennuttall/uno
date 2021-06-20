import pytest

from uno.card import UnoCard


def test_invalid_cards():
    with pytest.raises(TypeError):
        card = UnoCard()

    with pytest.raises(TypeError):
        card = UnoCard('black')

    with pytest.raises(ValueError):
        card = UnoCard('purple', 'ace')

    with pytest.raises(ValueError):
        card = UnoCard('red', 'ace')

    with pytest.raises(ValueError):
        card = UnoCard('purple', 1)

    with pytest.raises(ValueError):
        card = UnoCard('red', 'wildcard')

    with pytest.raises(ValueError):
        card = UnoCard('black', 1)

def test_valid_cards():
    card1 = UnoCard('red', 0)
    assert repr(card1) == '<UnoCard object: red 0>'
    card2 = UnoCard('red', 1)
    assert repr(card2) == '<UnoCard object: red 1>'
    assert card1 != card2
    assert card1.color == card2.color
    assert card1.card_type != card2.card_type
    card3 = UnoCard('red', 0)
    assert card1 == card3

def test_placing_cards():
    card1 = UnoCard('red', 1)

    card2 = UnoCard('red', 1)
    assert card1.playable(card2)
    card2 = UnoCard('red', 2)
    assert card1.playable(card2)
    card2 = UnoCard('red', 'skip')
    assert card1.playable(card2)
    card2 = UnoCard('green', 1)
    assert card1.playable(card2)
    card2 = UnoCard('green', 1)
    assert card1.playable(card2)
    card2 = UnoCard('red', 1)
    assert card1.playable(card2)
    card2 = UnoCard('black', 'wildcard')
    assert card1.playable(card2)
    card2 = UnoCard('black', '+4')
    assert card1.playable(card2)

def test_placing_invalid_cards():
    card1 = UnoCard('red', 1)

    card2 = UnoCard('green', 2)
    assert not card1.playable(card2)
    card2 = UnoCard('blue', 9)
    assert not card1.playable(card2)
    card2 = UnoCard('yellow', 'skip')
    assert not card1.playable(card2)

def test_placing_valid_cards_on_black_cards():
    card1 = UnoCard('black', 'wildcard')
    card1.temp_color = 'red'

    card2 = UnoCard('red', 1)
    assert card1.playable(card2)
    card2 = UnoCard('red', 'skip')
    assert card1.playable(card2)
    card2 = UnoCard('black', 'wildcard')
    assert card1.playable(card2)

def test_placing_invalid_cards_on_black_cards():
    card1 = UnoCard('black', 'wildcard')
    card1.temp_color = 'red'

    card2 = UnoCard('green', 1)
    assert not card1.playable(card2)

    card2 = UnoCard('green', 'skip')
    assert not card1.playable(card2)