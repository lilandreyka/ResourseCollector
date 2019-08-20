import arcade
import random
from math import sin, cos, radians

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900


class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.speed = 0
        self.ang = 0
        self.size = 40
        self.color = arcade.color.BLOND

    def turn_left(self):
        self.ang -= 10
        self.dx = sin(radians(self.ang))
        self.dy = cos(radians(self.ang))

    def turn_right(self):
        self.ang += 10
        self.dx = sin(radians(self.ang))
        self.dy = cos(radians(self.ang))

    def speed_up(self):
        if self.speed < 5:
            self.speed += 1

    def speed_down(self):
        if self.speed >= 0:
            self.speed -= 1

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.size, self.size,
                                     [100, 0, 0])
        pass


class Background:
    def __init__(self):
        self.img = arcade.load_texture("img/6561457.gif")

    def draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.img)

class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Настроить игру здесь
        self.robot = Robot(100, 250)
        pass

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.robot.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
             self.robot.turn_left()
        if symbol == arcade.key.RIGHT:
             self.robot.turn_right()
        if symbol == arcade.key.UP:
             self.robot.speed_up()
        if symbol == arcade.key.DOWN:
             self.robot.speed_down()


    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        self.robot.move()
        pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()