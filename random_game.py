from uno import UnoGame, COLORS
import random

players = random.randint(2, 15)
game = UnoGame(players)

print("Starting a {} player game".format(players))

count = 0
while game.is_active:
    count += 1
    player = game.current_player
    player_id = player.player_id
    if player.can_play(game.current_card):
        for i, card in enumerate(player.hand):
            if game.current_card.playable(card):
                if card.color == 'black':
                    new_color = random.choice(COLORS)
                else:
                    new_color = None
                print("Player {} played {}".format(player, card))
                game.play(player=player_id, card=i, new_color=new_color)
                break
    else:
        print("Player {} picked up".format(player))
        game.play(player=player_id, card=None)

print("{} player game - {} cards played".format(players, count))
