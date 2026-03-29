import pgzero.clock
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
_pending_card_index = None


def _init():
    global _game, _deck_img, _color_imgs
    _game = AIUnoGame(NUM_PLAYERS)
    _deck_img = Actor("back")
    _color_imgs = {color: Actor(color) for color in COLORS}
    pgzero.clock.schedule_interval(_advance_game, 1)


def _advance_game():
    if _game.game.is_active and _game.game.current_player != _game.player:
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
    global _pending_card_index
    if _game is None or _game.player != _game.game.current_player:
        return
    if _game.game_data.color_selection_required:
        for color, card in _color_imgs.items():
            if card.collidepoint(pos):
                _game.game_data.color_selection_required = False
                _game.play_human(_pending_card_index, new_color=color)
                _pending_card_index = None
        return
    for card in _game.player.hand:
        if card.sprite.collidepoint(pos):
            card_index = _game.player.hand.index(card)
            if card.color == "black" and len(_game.player.hand) > 1:
                _pending_card_index = card_index
                _game.game_data.color_selection_required = True
            else:
                _game.play_human(card_index)
            return
    if _deck_img.collidepoint(pos):
        _game.play_human(None)


def main():
    import pgzrun

    pgzrun.go()


if __name__ == "__main__":
    main()
