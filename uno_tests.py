import pytest
from uno import *

# Test creating invalid cards throws exception

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

# Test creating valid cards

card = UnoCard('red', 0)
card = UnoCard('black', 'wildcard')

# Test placing valid cards on other cards

card1 = UnoCard('red', 1)

card2 = UnoCard('red', 1)
assert card1.place(card2)
card2 = UnoCard('red', 2)
assert card1.place(card2)
card2 = UnoCard('red', 'skip')
assert card1.place(card2)
card2 = UnoCard('green', 1)
assert card1.place(card2)
card2 = UnoCard('green', 1)
assert card1.place(card2)
card2 = UnoCard('red', 1)
assert card1.place(card2)
card2 = UnoCard('black', 'wildcard')
assert card1.place(card2)
card2 = UnoCard('black', '+4')
assert card1.place(card2)

# Test placing invalid cards on other cards

card1 = UnoCard('red', 1)

card2 = UnoCard('green', 2)
assert not card1.place(card2)
card2 = UnoCard('blue', 9)
assert not card1.place(card2)
card2 = UnoCard('yellow', 'skip')
assert not card1.place(card2)

# Test placing valid cards on black cards

card1 = UnoCard('black', 'wildcard')
card1.temp_color = 'red'

card2 = UnoCard('red', 1)
assert card1.place(card2)
card2 = UnoCard('red', 'skip')
assert card1.place(card2)
card2 = UnoCard('black', 'wildcard')
assert card1.place(card2)

# Test placing invalid cards on black cards

card1 = UnoCard('black', 'wildcard')
card1.temp_color = 'red'

card2 = UnoCard('green', 1)
assert not card1.place(card2)

card2 = UnoCard('green', 'skip')
assert not card1.place(card2)

# Test creating invalid Uno Game

with pytest.raises(TypeError):
    game = UnoGame()

with pytest.raises(ValueError):
    game = UnoGame(1)

with pytest.raises(ValueError):
    game = UnoGame('foo')

with pytest.raises(TypeError):
    game = UnoGame('red', 1)

card = UnoCard('red', 1)
with pytest.raises(ValueError):
    game = UnoGame(card)

# Test creating valid Uno Game

for n in range(2, 8):
    game = UnoGame(n)
    assert len(game.players) == n
    for player in game.players:
        assert len(player) == 7
        for card in player:
            assert isinstance(card, UnoCard)
    assert len(game.deck) == 108 - 7*n

# Test gameplay

game = UnoGame(2)
assert isinstance(game.current_card, UnoCard)
assert game.is_active
