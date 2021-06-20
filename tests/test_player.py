import pytest

from uno.player import UnoPlayer
from uno.card import UnoCard

def test_creating_invalid_uno_player():
    cards = []
    with pytest.raises(ValueError):
        player = UnoPlayer(cards)

    cards = range(7)
    with pytest.raises(ValueError):
        player = UnoPlayer(cards)

    cards = [UnoCard('red', 0)]
    with pytest.raises(ValueError):
        player = UnoPlayer(cards)

    cards = [
        ('red', 0),
        ('red', 1),
        ('yellow', 0),
        ('yellow', 2),
        ('blue', 0),
        ('blue', 1),
    ]
    uno_cards = [UnoCard(color, card_type) for color, card_type in cards]
    uno_cards.append(1)
    with pytest.raises(ValueError):
        player = UnoPlayer(cards)

    cards = [
        ('red', 0),
        ('red', 1),
        ('yellow', 0),
        ('yellow', 2),
        ('blue', 0),
        ('blue', 1),
        ('black', 'wildcard'),
        ('black', '+4'),
    ]
    uno_cards = [UnoCard(color, card_type) for color, card_type in cards]
    with pytest.raises(ValueError):
        player = UnoPlayer(cards)

def test_creating_valid_uno_player():
    cards = [
        ('red', 0),
        ('red', 1),
        ('yellow', 0),
        ('yellow', 2),
        ('blue', 0),
        ('blue', 1),
        ('black', 'wildcard'),
    ]
    uno_cards = [UnoCard(color, card_type) for color, card_type in cards]
    player = UnoPlayer(uno_cards)