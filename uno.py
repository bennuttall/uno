from random import shuffle
from itertools import product, repeat, chain


COLORS = ['red', 'yellow', 'green', 'blue']
ALL_COLORS = COLORS + ['black']
NUMBERS = list(range(10)) + list(range(1, 10))
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES * 2
BLACK_CARD_TYPES = ['wildcard', '+4']
CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES


class UnoCard:
    """
    Represents a single Uno Card

    card = UnoCard(color, card_type)
    """
    def __init__(self, color, card_type):
        self._validate(color, card_type)
        self.color = color
        self.card_type = card_type
        self.temp_color = None

    def __repr__(self):
        return '<UnoCard object: {} {}>'.format(self.color, self.card_type)

    def __str__(self):
        return '{}{}>'.format(self.color_short, self.card_type_short)

    def __eq__(self, other):
        return self.color == other.color and self.card_type == other.card_type

    def _validate(self, color, card_type):
        """
        Check the card is valid, raise exception if not
        """
        if color not in ALL_COLORS:
            raise ValueError('Invalid color')
        if color == 'black' and card_type not in BLACK_CARD_TYPES:
            raise ValueError('Invalid card type')
        if color != 'black' and card_type not in COLOR_CARD_TYPES:
            raise ValueError('Invalid card type')

    @property
    def color_short(self):
        return self.color[0].upper()

    @property
    def card_type_short(self):
        if self.card_type in ('skip', 'reverse', 'wildcard'):
            return self.card_type[0].upper()
        else:
            return self.card_type

    @property
    def _color(self):
        return self.temp_color if self.temp_color else self.color

    @property
    def temp_color(self):
        return self._temp_color

    @temp_color.setter
    def temp_color(self, color):
        if color is not None:
            if color not in COLORS:
                raise ValueError('Invalid color')
        self._temp_color = color

    def playable(self, other):
        """
        Return True if the other card is playable on top of this card,
        otherwise return False
        """
        return (
            self._color == other.color or
            self.card_type == other.card_type or
            other.color == 'black'
        )


class UnoPlayer:
    """
    Represents a player in an Uno game. A player is created with a list of 7
    Uno cards.

    cards = [UnoCard('red', n) for n in range(7)]
    player = UnoPlayer(cards)
    """
    def __init__(self, cards):
        if len(cards) != 7:
            raise ValueError(
                'Invalid player: must be initalised with 7 UnoCards'
            )
        if not all(isinstance(card, UnoCard) for card in cards):
            raise ValueError(
                'Invalid player: cards must all be UnoCard objects'
            )
        self.hand = cards

    def can_go(self, current_card):
        """
        Return True if the player has any playable cards (on top of the current
        card provided), otherwise return False
        """
        return any(current_card.playable(card) for card in self.hand)


class UnoGame:
    def __init__(self, players, random=True):
        self.random = random
        if not isinstance(players, int):
            raise ValueError('Invalid game: players must be integer')
        if players < 2:
            raise ValueError('Invalid game: must be at least 2 players')
        self.deck = self._create_deck()
        self.players = [
            UnoPlayer(self._deal_hand()) for player in range(players)
        ]

    def _create_deck(self):
        color_cards = product(COLORS, COLOR_CARD_TYPES)
        black_cards = product(repeat('black', 4), BLACK_CARD_TYPES)
        all_cards = chain(color_cards, black_cards)
        deck = [UnoCard(color, card_type) for color, card_type in all_cards]
        if self.random:
            shuffle(deck)
            return deck
        else:
            return list(reversed(deck))

    def _deal_hand(self):
        return [self.deck.pop() for i in range(7)]

    @property
    def current_card(self):
        return self.deck[-1]

    @property
    def is_active(self):
        return True

    @property
    def current_player(self):
        return self.players[0]

    def play(self, player, card):
        if not isinstance(player, int):
            raise ValueError('Invalid player: should be the index')
        if not 0 <= player < len(self.players):
            raise ValueError('Invalid player: index out of range')
        _player = self.players[player]
        if self.current_player != _player:
            raise ValueError('Invalid player: not their turn')
        _card = _player.hand[card]
        if not self.current_card.playable(_card):
            raise ValueError(
                'Invalid card: {} not playable on {}'.format(
                    _card, self.current_card
                )
            )
        played_card = _player.hand.pop(card)
        self.deck.append(played_card)
