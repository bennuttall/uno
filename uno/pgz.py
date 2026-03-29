from itertools import chain, product, repeat
from pathlib import Path
from random import choice, shuffle as random_shuffle

import pgzero.loaders
from pgzero.actor import Actor

pgzero.loaders.images = pgzero.loaders.ImageLoader(str(Path(__file__).parent / "images"))

from .card import UnoCard
from .constants import BLACK_CARD_TYPES, COLOR_CARD_TYPES, COLORS
from .game import UnoGame


class PgzUnoCard(UnoCard):
    def __init__(self, color, card_type):
        super().__init__(color, card_type)
        self.sprite = Actor("{}_{}".format(color, card_type))

    def __format__(self, f):
        if f == "full":
            return "{} {}".format(self.color, self.card_type)
        else:
            return str(self)


class PgzUnoGame(UnoGame):
    def __init__(self, players, random=True):
        super().__init__(players, random)
        self._check_first_card()

    def _create_deck(self, random):
        color_cards = product(COLORS, COLOR_CARD_TYPES)
        black_cards = product(repeat("black", 4), BLACK_CARD_TYPES)
        deck = [PgzUnoCard(c, t) for c, t in chain(color_cards, black_cards)]
        if random:
            random_shuffle(deck)
            return deck
        return list(reversed(deck))

    def _check_first_card(self):
        if self.current_card.color == "black":
            color = choice(COLORS)
            self.current_card.temp_color = color
            print("Selected random color for black card: {}".format(color))


class GameData:
    def __init__(self):
        self.color_selection_required = False
        self.log = ""


class AIUnoGame:
    def __init__(self, players):
        self.game = PgzUnoGame(players)
        self.player = choice(self.game.players)
        self.player_index = self.game.players.index(self.player)
        self.game_data = GameData()
        print("The game begins. You are Player {}.".format(self.player_index))

    def __next__(self):
        """Advance the game for AI players. Returns without action on the human's turn."""
        game = self.game
        game_data = self.game_data
        player = game.current_player
        player_id = player.player_id
        if player == self.player:
            return
        elif player.can_play(game.current_card):
            for i, card in enumerate(player.hand):
                if game.current_card.playable(card):
                    if card.color == "black":
                        new_color = choice(COLORS)
                    else:
                        new_color = None
                    game_data.log = "Player {} played {:full}".format(player, card)
                    game.play(player=player_id, card=i, new_color=new_color)
                    break
        else:
            game_data.log = "Player {} picked up".format(player)
            game.play(player=player_id, card=None)

    def play_human(self, card_index, new_color=None):
        """Play the human's turn. Returns False if the card is not playable."""
        player = self.player
        game_data = self.game_data
        if card_index is not None:
            card = player.hand[card_index]
            if not self.game.current_card.playable(card):
                game_data.log = "You cannot play that card"
                return False
            game_data.log = "You played card {:full}".format(card)
        else:
            game_data.log = "You picked up"
        self.game.play(player.player_id, card_index, new_color)
        return True

    def print_hand(self):
        print("Your hand: {}".format(" ".join(str(card) for card in self.player.hand)))
