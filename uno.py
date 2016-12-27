import random


COLORS = ['red', 'yellow', 'green', 'blue']
ALL_COLORS = COLORS + ['black']
NUMBERS = list(range(10)) + list(range(1, 10))
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES * 2
BLACK_CARD_TYPES = ['colorswap', '+4']
CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES


class UnoCard:
    def __init__(self, color, card_type):
        if color not in ALL_COLORS:
            raise ValueError('Invalid color')
        self.color = color

        if card_type not in CARD_TYPES:
            raise ValueError('Invalid card type')
        if color == 'black' and card_type not in BLACK_CARD_TYPES:
            raise ValueError('Invalid card type')
        if color != 'black' and card_type in BLACK_CARD_TYPES:
            raise ValueError('Invalid card type')
        self.card_type = card_type


def create_uno_deck():
    deck = []
    for color in COLORS:
        for card_type in COLOR_CARD_TYPES:
            deck.append(UnoCard(color, card_type))
    for card_type in BLACK_CARD_TYPES:
        for i in range(4):
            deck.append(UnoCard('black', card_type))

    random.shuffle(deck)
    return deck
