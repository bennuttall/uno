import pytest

from uno import UnoCard, UnoPlayer


# Test creating invalid Uno Player

def test_player_requires_cards():
    with pytest.raises(ValueError):
        UnoPlayer([])


def test_player_cards_must_be_uno_cards():
    with pytest.raises(ValueError):
        UnoPlayer(range(7))


def test_player_requires_seven_cards():
    with pytest.raises(ValueError):
        UnoPlayer([UnoCard("red", 0)])


def test_player_cards_must_not_include_non_uno_cards():
    cards = [
        ("red", 0), ("red", 1), ("yellow", 0),
        ("yellow", 2), ("blue", 0), ("blue", 1),
    ]
    uno_cards = [UnoCard(color, card_type) for color, card_type in cards]
    uno_cards.append(1)
    with pytest.raises(ValueError):
        UnoPlayer(cards)


def test_player_requires_exactly_seven_cards():
    cards = [
        ("red", 0), ("red", 1), ("yellow", 0), ("yellow", 2),
        ("blue", 0), ("blue", 1), ("black", "wildcard"), ("black", "+4"),
    ]
    uno_cards = [UnoCard(color, card_type) for color, card_type in cards]
    with pytest.raises(ValueError):
        UnoPlayer(cards)


# Test creating valid Uno Player

def test_player_valid():
    cards = [
        ("red", 0), ("red", 1), ("yellow", 0), ("yellow", 2),
        ("blue", 0), ("blue", 1), ("black", "wildcard"),
    ]
    uno_cards = [UnoCard(color, card_type) for color, card_type in cards]
    player = UnoPlayer(uno_cards)
    assert len(player.hand) == 7
