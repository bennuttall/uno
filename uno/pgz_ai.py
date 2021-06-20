from random import choice

from uno.game import UnoGame
from uno.data import GameData
from uno.const import COLORS


class AIUnoGame:
    def __init__(self, players):
        self.game = UnoGame(players)
        self.player = choice(self.game.players)
        self.player_index = self.game.players.index(self.player)
        self.data = GameData()
        print('The game begins. You are Player {}.'.format(self.player_index))

    def __next__(self):
        game = self.game
        player = game.current_player
        player_id = player.player_id
        current_card = game.current_card
        if player == self.player:
            played = False
            while not played:
                card_index = None
                while card_index is None:
                    card_index = self.data.selected_card
                new_color = None
                if card_index is not False:
                    card = player.hand[card_index]
                    if not game.current_card.playable(card):
                        self.data.log = 'You cannot play that card'
                        continue
                    else:
                        self.data.log = 'You played card {:full}'.format(card)
                        if card.color == 'black' and len(player.hand) > 1:
                            self.data.color_selection_required = True
                            while new_color is None:
                                new_color = self.data.selected_color
                            self.data.log = 'You selected {}'.format(new_color)
                else:
                    card_index = None
                    self.data.log = 'You picked up'
                game.play(player_id, card_index, new_color)
                played = True
        elif player.can_play(game.current_card):
            for i, card in enumerate(player.hand):
                if game.current_card.playable(card):
                    if card.color == 'black':
                        new_color = choice(COLORS)
                    else:
                        new_color = None
                    self.data.log = "Player {} played {:full}".format(player, card)
                    game.play(player=player_id, card=i, new_color=new_color)
                    break
        else:
            self.data.log = "Player {} picked up".format(player)
            game.play(player=player_id, card=None)


    def print_hand(self):
        print('Your hand: {}'.format(
            ' '.join(str(card) for card in self.player.hand)
        ))