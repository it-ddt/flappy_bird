"""Модуль труб."""

import random

import arcade

import config


class Pipes(arcade.SpriteList):
    """Менеджер труб."""
    def __init__(self, window_width: int, window_height: int, bird_height: float):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.pipe_height = self.window_height * 0.9
        self.gap = bird_height * 3
        self.shift_min = int(self.window_height * 0.15) * -1
        self.shift_max = int(self.window_height * 0.3)
        self.spawn_interval = 2
        self.spawn_timer = self.spawn_interval

    def update(self, delta_time):
        for pipe in self:
            pipe.update(delta_time)
        self.spawn_timer += delta_time
        if self.spawn_timer < self.spawn_interval:
            return
        self.spawn()
        self.spawn_timer = 0

    def spawn(self):
        """Создает пару труб за правой границей экрана."""
        shift_y = random.randint(self.shift_min, self.shift_max)

        # нижняя труба
        pipe_lower = Pipe()
        pipe_lower.height = self.pipe_height
        pipe_lower.width = self.pipe_height * pipe_lower.proportion
        pipe_lower.left = self.window_width
        pipe_lower.top = self.window_height * 0.5 - self.gap / 2
        pipe_lower.center_y += shift_y
        self.append(pipe_lower)

        # верхняя труба
        pipe_upper = Pipe(is_flipped=True)
        pipe_upper.height = self.pipe_height
        pipe_upper.width = self.pipe_height * pipe_lower.proportion
        pipe_upper.left = self.window_width
        pipe_upper.bottom = self.window_height * 0.5 + self.gap / 2
        pipe_upper.center_y += shift_y
        pipe_upper.is_score = False
        self.append(pipe_upper)


class Pipe(arcade.Sprite):
    def __init__(self, is_flipped = False):
        super().__init__()
        self.texture = arcade.load_texture(config.DIR_IMG / "pipe-green.png")
        if is_flipped:
            self.texture = self.texture.flip_vertically()
        self.proportion = self.texture.width / self.texture.height
        self.vel_x = 300
        self.is_score = True  # может дать балл

    def update(self, delta_time):
        self.center_x -= self.vel_x * delta_time

        # удаляет трубы, которые уехали за левую границу экрана
        if self.right <= 0:
            self.remove_from_sprite_lists()

