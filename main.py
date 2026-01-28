"""
TODO: сделать EXE файл
"""

import arcade

from game_view import GameView

if __name__ == "__main__":
    window = arcade.Window(
        fullscreen=True,
        update_rate=1/60,
        draw_rate=1/60,
    )
    view = GameView()
    window.show_view(view)
    arcade.run()
