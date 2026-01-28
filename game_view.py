"""Модуль представления игры."""

import arcade

from bird import Bird
import config
from layers import ScrollingLayer
from pipes import Pipes
from sprites import Score_HUD, Splash


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # спрайты
        self.sprites = arcade.SpriteList()
        self.splash = arcade.SpriteList()
        self.score_hud = Score_HUD(self.width, self.height)
        self.bird = Bird(self.width, self.height)
        self.bg = ScrollingLayer(self.width, self.height, "background-day.png", 1, 100)
        self.ground = ScrollingLayer(self.width, self.height, "base.png", 0.2, 200)
        self.pipes = Pipes(self.width, self.height, self.bird.height)
        self.score = 0
        self.sprites.append(self.bird)
        intro = Splash(self.width, self.height, "intro.png", 0.7)
        music = arcade.load_sound(config.DIR_SOUND / "music.mp3")
        self.music_player = music.play(loop=True, volume=0.03)
        self.splash.append(intro)
        self.is_paused = True
        self.setup()

    def setup(self) -> None:
        """Приводит игру в изначальное состояние."""
        self.pipes.clear()
        self.score = 99
        self.bird.setup()

    def on_draw(self):
        """Рисует все спрайты."""
        self.clear()
        self.bg.draw()
        self.ground.draw()
        self.pipes.draw()
        self.sprites.draw()
        self.score_hud.draw()
        if self.is_paused:
            self.splash.draw()
        arcade.draw_line(self.width // 2, 0, self.width // 2, self.height, color=arcade.color.PURPLE)

    def on_update(self, delta_time):
        if self.is_paused:
            return
        if self.is_collide_pipes():
            return
        if self.is_collide_ground():
            return
        self.bg.update(delta_time)
        self.ground.update(delta_time)
        self.change_score()
        self.bird.update(delta_time)
        self.score_hud.update(delta_time, self.score)
        self.pipes.update(delta_time)

    def is_collide_pipes(self) -> bool:
        """Коллизия птицы с трубами."""
        if not arcade.check_for_collision_with_list(self.bird, self.pipes):
            return False
        self.bird.is_acitve = False
        self.is_paused = True
        self.splash.clear()  # TODO: cделать один раз
        sprite = Splash(self.width, self.height, "gameover.png", 0.1)
        self.splash.append(sprite)
        arcade.play_sound(self.bird.sounds["hit"])
        return True

    def is_collide_ground(self) -> bool:
        """Коллизия с землей."""
        if self.bird.bottom > self.ground.height:
            return False
        self.bird.bottom = self.ground.height

        self.bird.is_acitve = False
        self.is_paused = True
        self.splash.clear()
        sprite = Splash(self.width, self.height, "gameover.png", 0.1)
        self.splash.append(sprite)
        arcade.play_sound(self.bird.sounds["hit"])
        return True

    def change_score(self) -> None:
        """Дает только 1 балл за пройденную нижнюю трубу."""
        for pipe in self.pipes:
            if pipe.center_x <= self.bird.center_x and pipe.is_score:
                self.score += 1
                pipe.is_score = False
                arcade.play_sound(self.bird.sounds["point"], volume=0.1)

    def on_key_press(self, symbol, _):
        if symbol == arcade.key.SPACE:
            if not self.bird.is_acitve:  # на врезавшейся птице
                self.setup()
                self.is_paused = False
            if self.is_paused:
                self.is_paused = False

        elif symbol == arcade.key.ESCAPE:
            arcade.exit()
        self.bird.on_key_press(symbol)

