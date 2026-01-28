"""Модуль птицы."""

import arcade

import config


class Bird(arcade.Sprite):
    def __init__(self, window_width: int, window_height: int):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.coords_initial = (int(self.window_width // 2), int(self.window_height // 2))

        self.textures = [
            arcade.load_texture(config.DIR_IMG / "yellowbird-upflap.png"),
            arcade.load_texture(config.DIR_IMG / "yellowbird-midflap.png"),
            arcade.load_texture(config.DIR_IMG / "yellowbird-downflap.png"),
            arcade.load_texture(config.DIR_IMG / "yellowbird-midflap.png"),
        ]

        self.texture_idx = 0
        self.texture = self.textures[self.texture_idx]
        self.proportion = self.texture.width / self.texture.height

        self.height = window_height * 0.05
        self.width = self.height * self.proportion

        self.vel_min = -400.0
        self.gravity = 900.0
        self.vel_jump = 300.0

        self.animation_timer = 0.0
        self.animation_frame_duration = 0.12  # хардкод?

        self.rotation_speed = 200.0
        self.angle_top = -25
        self.angle_bottom = 90

        self.sounds = dict()
        sounds = ("wing", "hit", "point")
        for sound in sounds:
            self.sounds[sound] = arcade.load_sound(config.DIR_SOUND / f"{sound}.ogg")

    def setup(self):
        """Возвращает птицу в исходное состояние."""
        self.center_x, self.center_y = self.coords_initial
        self.vel_y = 0.0
        self.angle = 0
        self.is_acitve = True

    def update(self, delta_time):
        if not self.is_acitve:
            return
        self.apply_gravity(delta_time)
        self.reposition(delta_time)
        self.collide_top()
        self.animate(delta_time)
        self.rotate(delta_time)

    def reposition(self, delta_time):
        self.center_y += self.vel_y * delta_time

    def collide_top(self) -> None:
        """Не выпускает птицу за верxнюю границу окна."""
        if self.top > self.window_height:
            self.top = self.window_height

    def jump(self):
        self.vel_y = self.vel_jump

    def apply_gravity(self, delta_time):
        self.vel_y -= self.gravity * delta_time
        self.vel_y = max(self.vel_y, self.vel_min)

    def animate(self, delta_time):
        self.animation_timer += delta_time

        if self.animation_timer < self.animation_frame_duration:
            return

        self.animation_timer = 0
        self.texture_idx = (self.texture_idx + 1) % len(self.textures)
        self.texture = self.textures[self.texture_idx]

    def rotate(self, delta_time):
        if self.vel_y > 0:
            self.angle = self.angle_top
            return

        angle_delta = self.angle_bottom - self.angle
        step = self.rotation_speed * delta_time

        if abs(angle_delta) < step:
            self.angle = self.angle_bottom
            return

        if angle_delta > 0:
            self.angle += step
            return

        self.angle -= step

    def on_key_press(self, symbol):
        if symbol == arcade.key.SPACE:
            self.jump()
            arcade.play_sound(self.sounds["wing"])


if __name__ == "__main__":
    def test() -> None:
        """Тест размеров экземпляра."""
        bird = Bird(1920, 1080)
        print(f"Создан экземпляр птицы размерами: {bird.width}×{bird.height}")


    test()
