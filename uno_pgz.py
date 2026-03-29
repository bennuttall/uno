from threading import Thread
from time import sleep

from pgzero.actor import Actor
from pgzero.screen import Screen as _Screen

from uno.constants import COLORS
from uno.pgz import AIUnoGame

WIDTH = 1200
HEIGHT = 800

NUM_PLAYERS = 3

screen: _Screen
_game = None
_deck_img = None
_color_imgs = None


def _init():
    global _game, _deck_img, _color_imgs
    _game = AIUnoGame(NUM_PLAYERS)
    _deck_img = Actor("back")
    _color_imgs = {color: Actor(color) for color in COLORS}
    Thread(target=_game_loop, daemon=True).start()


def _game_loop():
    while _game.game.is_active:
        sleep(1)
        next(_game)


def update():
    if _game is None:
        _init()
    screen.clear()
    screen.fill((255, 255, 255))
    _draw_deck()
    _draw_players_hands()
    _show_log()


def _draw_deck():
    _deck_img.pos = (130, 70)
    _deck_img.draw()
    current_card = _game.game.current_card
    current_card.sprite.pos = (210, 70)
    current_card.sprite.draw()
    if _game.game_data.color_selection_required:
        for i, card in enumerate(_color_imgs.values()):
            card.pos = (290 + i * 80, 70)
            card.draw()
    elif current_card.color == "black" and current_card.temp_color is not None:
        color_img = _color_imgs[current_card.temp_color]
        color_img.pos = (290, 70)
        color_img.draw()


def _draw_players_hands():
    for p, player in enumerate(_game.game.players):
        color = "red" if player == _game.game.current_player else "black"
        text = "P{} {}".format(p, "wins" if _game.game.winner == player else "")
        screen.draw.text(text, (0, 300 + p * 130), fontsize=100, color=color)
        for c, card in enumerate(player.hand):
            if player == _game.player:
                sprite = card.sprite
            else:
                sprite = Actor("back")
            sprite.pos = (130 + c * 80, 330 + p * 130)
            sprite.draw()


def _show_log():
    screen.draw.text(_game.game_data.log, midbottom=(WIDTH / 2, HEIGHT - 50), color="black")


def on_mouse_down(pos):
    if _game is None or _game.player != _game.game.current_player:
        return
    for card in _game.player.hand:
        if card.sprite.collidepoint(pos):
            _game.game_data.selected_card = _game.player.hand.index(card)
            print("Selected card {} index {}".format(card, _game.player.hand.index(card)))
    if _deck_img.collidepoint(pos):
        _game.game_data.selected_card = False
        print("Selected pick up")
    for color, card in _color_imgs.items():
        if card.collidepoint(pos):
            _game.game_data.selected_color = color
            _game.game_data.color_selection_required = False


def main():
    import pgzrun

    pgzrun.go()


if __name__ == "__main__":
    main()
