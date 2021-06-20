from .const import COLORS, ALL_COLORS, BLACK_CARD_TYPES, COLOR_CARD_TYPES
from pgzero.actor import Actor


class UnoCard:
    """
    Represents a single Uno Card, given a valid color and card type.

    color: string
    card_type: string/int

    >>> card = UnoCard('red', 5)
    """
    def __init__(self, color, card_type):
        self._validate(color, card_type)
        self.color = color
        self.card_type = card_type
        self.temp_color = None
        self._sprite = None

    def __repr__(self):
        return '<UnoCard object: {} {}>'.format(self.color, self.card_type)

    def __str__(self):
        return '{}{}'.format(self.color_short, self.card_type_short)

    def __format__(self, f):
        if f == 'full':
            return '{} {}'.format(self.color, self.card_type)
        else:
            return str(self)

    def __eq__(self, other):
        return self.color == other.color and self.card_type == other.card_type

    def _validate(self, color, card_type):
        """
        Check the card is valid, raise exception if not.
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

    @property
    def sprite(self):
        if self._sprite is None:
            self._sprite = Actor('{}_{}'.format(self.color, self.card_type))
        return self._sprite
        

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