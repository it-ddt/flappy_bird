"""Модуль спрайтов."""


import arcade

import config


class Splash(arcade.Sprite):
    def __init__(self, window_width: int, window_height: int, filename: str, scale: float):
        super().__init__()
        self.texture = arcade.load_texture(config.DIR_IMG / filename)
        proportion = self.texture.width / self.texture.height
        self.height = int(window_height * scale)
        self.width = self.height * proportion
        self.center_x = window_width // 2
        self.center_y = window_height // 2


class Score_HUD(arcade.SpriteList):
    """Счет поверх экрана."""

    def __init__(self, window_width: int, window_height: int):
        super().__init__()
        self.start_x = int(window_width // 2)
        self.start_y = int(window_height * 0.9)
        self.textures = []
        for i in range(10):
            texture = arcade.load_texture(config.DIR_IMG / f"{i}.png")
            self.textures.append(texture)
        self.proportion = self.textures[0].width / self.textures[0].height
        self.height = int(window_height * 0.2)
        self.width = self.height * self.proportion
        # TODO: центрировать счет

    def update(self, delta_time: float, score: int):
        self.clear()

        spacing = 0.3  # <1 — цифры ближе, =1 — вплотную, >1 — дальше
        width_total = self.width * spacing * len(str(score))
        x = self.start_x - width_total / 2 + (self.width * spacing) / 2

        for ch in str(score):
            sprite = arcade.Sprite()
            sprite.texture = self.textures[int(ch)]
            sprite.center_x = x
            sprite.center_y = self.start_y

            self.append(sprite)
            x += self.width * spacing
