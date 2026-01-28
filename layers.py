"""Модуль слоев."""

import arcade

import config


class ScrollingLayer(arcade.SpriteList):
    """Слой с бесконечной прокруткой спрайтов."""
    def __init__(
            self,
            window_width: int,
            window_height: int,
            texture_name: str,
            window_portion: float,
            speed: float,
    ):
        super().__init__()
        texture = arcade.load_texture(config.DIR_IMG / texture_name)
        proportion = texture.width / texture.height
        self.height = window_height * window_portion
        self.width = self.height * proportion
        self.speed = speed

        number = int(window_width / self.width) + 2
        for i in range(number):
            sprite = arcade.Sprite(texture)
            sprite.width = self.width
            sprite.height = self.height
            sprite.left = self.width * i
            sprite.bottom = 0
            self.append(sprite)

    def update(self, delta_time):
        for sprite in self:
            sprite.center_x -= self.speed * delta_time

        first_sprite = self[0]

        if first_sprite.right < 0:
            last_sprite = self[-1]
            first_sprite.left = last_sprite.right
            self.remove(first_sprite)
            self.append(first_sprite)

