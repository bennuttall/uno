import pytest
from uno import *

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

card = UnoCard('red', 0)
card = UnoCard('black', 'colorswap')

with pytest.raises(ValueError):
    card = UnoCard('red', 'colorswap')

with pytest.raises(ValueError):
    card = UnoCard('black', 1)

deck = create_uno_deck()
assert len(deck) == 108
