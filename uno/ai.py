from random import choice

from .game import UnoGame
from .const import COLORS


class AIUnoGame:
    def __init__(self, players):
        self.game = UnoGame(players)
        self.player = choice(self.game.players)
        self.player_index = self.game.players.index(self.player)
        print('The game begins. You are Player {}.'.format(self.player_index))
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
            print('Current card: {}, color: {}'.format(
                game.current_card, game.current_card._color
            ))
            self.print_hand()
            if player.can_play(current_card):
                played = False
                while not played:
                    card_index = int(input('Which card do you want to play? '))
                    card = player.hand[card_index]
                    if not game.current_card.playable(card):
                        print('Cannot play that card')
                    else:
                        if card.color == 'black':
                            new_color = input('Which color do you want? ')
                        else:
                            new_color = None
                        game.play(player_id, card_index, new_color)
                        played = True
            else:
                print('You cannot play. You must pick up a card.')
                game.play(player_id, card=None)
                self.print_hand()
        elif player.can_play(game.current_card):
            for i, card in enumerate(player.hand):
                if game.current_card.playable(card):
                    if card.color == 'black':
                        new_color = choice(COLORS)
                    else:
                        new_color = None
                    print("Player {} played {}".format(player, card))
                    game.play(player=player_id, card=i, new_color=new_color)
                    break
        else:
            print("Player {} picked up".format(player))
            game.play(player=player_id, card=None)

    def print_hand(self):
        print('Your hand: {}'.format(
            ' '.join(str(card) for card in self.player.hand)
        ))