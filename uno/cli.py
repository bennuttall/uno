from argparse import ArgumentParser
from random import choice

from .constants import COLORS
from .game import UnoGame


class CLIUnoGame:
    def __init__(self, players):
        self.game = UnoGame(players)
        self.player = choice(self.game.players)
        self.player_index = self.game.players.index(self.player)
        print("The game begins. You are Player {}.".format(self.player_index))
        self.print_hand()
        while self.game.is_active:
            print()
            next(self)

    def __next__(self):
        game = self.game
        player = game.current_player
        player_id = player.player_id
        current_card = game.current_card
        if player == self.player:
            print("Current card: {}, color: {}".format(game.current_card, game.current_card._color))
            self.print_hand()
            if player.can_play(current_card):
                played = False
                while not played:
                    choice_input = input("Which card do you want to play? (1-{}, or p to pick up) ".format(len(player.hand)))
                    if choice_input == "p":
                        game.play(player_id, card=None)
                        played = True
                    elif choice_input.isdigit() and 1 <= int(choice_input) <= len(player.hand):
                        card_index = int(choice_input) - 1
                        card = player.hand[card_index]
                        if not game.current_card.playable(card):
                            print("Cannot play that card")
                        else:
                            if card.color == "black":
                                new_color = self._pick_color()
                            else:
                                new_color = None
                            game.play(player_id, card_index, new_color)
                            played = True
                    else:
                        print("Invalid input")
            else:
                print("You cannot play. You must pick up a card.")
                game.play(player_id, card=None)
                self.print_hand()
        elif player.can_play(game.current_card):
            for i, card in enumerate(player.hand):
                if game.current_card.playable(card):
                    if card.color == "black":
                        new_color = choice(COLORS)
                    else:
                        new_color = None
                    print("Player {} played {}".format(player, card))
                    game.play(player=player_id, card=i, new_color=new_color)
                    break
        else:
            print("Player {} picked up".format(player))
            game.play(player=player_id, card=None)

    def _pick_color(self):
        for i, color in enumerate(COLORS, 1):
            print("{}. {}".format(i, color))
        while True:
            choice_input = input("Which color do you want? (1-{}) ".format(len(COLORS)))
            if choice_input.isdigit() and 1 <= int(choice_input) <= len(COLORS):
                return COLORS[int(choice_input) - 1]
            print("Invalid input")

    def print_hand(self):
        for i, card in enumerate(self.player.hand, 1):
            print("{}. {}".format(i, card))


def main():
    parser = ArgumentParser()
    parser.add_argument("--players", type=int, default=3)
    args = parser.parse_args()
    CLIUnoGame(args.players)
