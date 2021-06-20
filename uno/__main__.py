# pylint: skip-file

from pgzrun import go as main

from threading import Thread
from time import sleep

from uno.pgz_ai import AIUnoGame
from uno.data import GameData
from uno.const import COLORS


WIDTH = 1200
HEIGHT = 800

num_players = 3

game = AIUnoGame(num_players)


def game_loop():
    while game.game.is_active:
        sleep(1)
        next(game)


def draw_deck():
    deck_img.pos = (130, 70)
    deck_img.draw()
    current_card = game.game.current_card
    current_card.sprite.pos = (210, 70)
    current_card.sprite.draw()
    if game.data.color_selection_required:
        for i, card in enumerate(color_imgs.values()):
            card.pos = (290+i*80, 70)
            card.draw()
    elif current_card.color == 'black' and current_card.temp_color is not None:
        color_img = color_imgs[current_card.temp_color]
        color_img.pos = (290, 70)
        color_img.draw()

def draw_players_hands():
    for p, player in enumerate(game.game.players):
        color = 'red' if player == game.game.current_player else 'black'
        text = 'P{} {}'.format(p, 'wins' if game.game.winner == player else '')
        screen.draw.text(text, (0, 300+p*130), fontsize=100, color=color)
        for c, card in enumerate(player.hand):
            if player == game.player:
                sprite = card.sprite
            else:
                sprite = Actor('back')
            sprite.pos = (130+c*80, 330+p*130)
            sprite.draw()

def show_log():
    screen.draw.text(game.data.log, midbottom=(WIDTH/2, HEIGHT-50), color='black')

def update():
    screen.clear()
    screen.fill((255, 255, 255))
    draw_deck()
    draw_players_hands()
    show_log()

def on_mouse_down(pos):
    if game.player == game.game.current_player:
        for card in game.player.hand:
            if card.sprite.collidepoint(pos):
                game.data.selected_card = game.player.hand.index(card)
                print('Selected card {} index {}'.format(card, game.player.hand.index(card)))
        if deck_img.collidepoint(pos):
            game.data.selected_card = False
            print('Selected pick up')
        for color, card in color_imgs.items():
            if card.collidepoint(pos):
                game.data.selected_color = color
                game.data.color_selection_required = False

deck_img = Actor('back')
color_imgs = {color: Actor(color) for color in COLORS}
game_loop_thread = Thread(target=game_loop)
game_loop_thread.start()

main()