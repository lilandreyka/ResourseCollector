import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Robot:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.dx = 0
        self.dy = 0
        self.size = 40
        self.color = arcade.color.BLOND

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
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
        pass

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
             pass
        if symbol == arcade.key.RIGHT:
            pass


    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()