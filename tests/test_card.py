import pytest

from uno import UnoCard


# Test creating invalid cards

def test_card_requires_arguments():
    with pytest.raises(TypeError):
        UnoCard()


def test_card_requires_two_arguments():
    with pytest.raises(TypeError):
        UnoCard("black")


def test_card_invalid_color_and_type():
    with pytest.raises(ValueError):
        UnoCard("purple", "ace")


def test_card_invalid_type_for_color():
    with pytest.raises(ValueError):
        UnoCard("red", "ace")


def test_card_invalid_color():
    with pytest.raises(ValueError):
        UnoCard("purple", 1)


def test_card_black_type_on_color_card():
    with pytest.raises(ValueError):
        UnoCard("red", "wildcard")


def test_card_color_type_on_black_card():
    with pytest.raises(ValueError):
        UnoCard("black", 1)


# Test creating valid cards

def test_card_repr():
    card = UnoCard("red", 0)
    assert repr(card) == "<UnoCard object: red 0>"


def test_card_equality():
    card1 = UnoCard("red", 0)
    card2 = UnoCard("red", 1)
    assert card1 != card2
    assert card1.color == card2.color
    assert card1.card_type != card2.card_type
    card3 = UnoCard("red", 0)
    assert card1 == card3


# Test placing valid cards on other cards

def test_playable_same_color_same_type():
    card1 = UnoCard("red", 1)
    assert card1.playable(UnoCard("red", 1))


def test_playable_same_color_different_type():
    card1 = UnoCard("red", 1)
    assert card1.playable(UnoCard("red", 2))


def test_playable_same_color_special():
    card1 = UnoCard("red", 1)
    assert card1.playable(UnoCard("red", "skip"))


def test_playable_different_color_same_type():
    card1 = UnoCard("red", 1)
    assert card1.playable(UnoCard("green", 1))


def test_playable_black_wildcard():
    card1 = UnoCard("red", 1)
    assert card1.playable(UnoCard("black", "wildcard"))


def test_playable_black_plus_four():
    card1 = UnoCard("red", 1)
    assert card1.playable(UnoCard("black", "+4"))


# Test placing invalid cards on other cards

def test_not_playable_different_color_different_type():
    card1 = UnoCard("red", 1)
    assert not card1.playable(UnoCard("green", 2))


def test_not_playable_different_color_different_type_2():
    card1 = UnoCard("red", 1)
    assert not card1.playable(UnoCard("blue", 9))


def test_not_playable_different_color_special():
    card1 = UnoCard("red", 1)
    assert not card1.playable(UnoCard("yellow", "skip"))


# Test placing valid cards on black cards with temp_color

def test_playable_on_black_same_temp_color():
    card1 = UnoCard("black", "wildcard")
    card1.temp_color = "red"
    assert card1.playable(UnoCard("red", 1))


def test_playable_on_black_special_same_temp_color():
    card1 = UnoCard("black", "wildcard")
    card1.temp_color = "red"
    assert card1.playable(UnoCard("red", "skip"))


def test_playable_on_black_another_black():
    card1 = UnoCard("black", "wildcard")
    card1.temp_color = "red"
    assert card1.playable(UnoCard("black", "wildcard"))


# Test placing invalid cards on black cards with temp_color

def test_not_playable_on_black_different_color():
    card1 = UnoCard("black", "wildcard")
    card1.temp_color = "red"
    assert not card1.playable(UnoCard("green", 1))


def test_not_playable_on_black_special_different_color():
    card1 = UnoCard("black", "wildcard")
    card1.temp_color = "red"
    assert not card1.playable(UnoCard("green", "skip"))
