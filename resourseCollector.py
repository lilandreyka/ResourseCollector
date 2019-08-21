import arcade
import random
from math import sin, cos, radians

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RESOURSE_COUNT = 4

def check_collision(obj1, obj2):

    ax1 = obj1.x - obj1.size / 2
    ay1 = obj1.y - obj1.size / 2
    ax2 = obj1.x + obj1.size / 2
    ay2 = obj1.y + obj1.size / 2

    bx1 = obj2.x - obj2.size / 2
    by1 = obj2.y - obj2.size / 2
    bx2 = obj2.x + obj2.size / 2
    by2 = obj2.y + obj2.size / 2

    s1 = (ax1 >= bx1 and ax1 <= bx2) or (ax2 >= bx1 and ax2 <= bx2)
    s2 = (ay1 >= by1 and ay1 <= by2) or (ay2 >= by1 and ay2 <= by2)
    s3 = (bx1 >= ax1 and bx1 <= ax2) or (bx2 >= ax1 and bx2 <= ax2)
    s4 = (by1 >= ay1 and by1 <= ay2) or (by2 >= ay1 and by2 <= ay2)

    return ((s1 and s2) or (s3 and s4)) or\
           ((s1 and s4) or (s3 and s2))


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
        self.ang -= 20
        self.dx = sin(radians(self.ang))
        self.dy = cos(radians(self.ang))

    def turn_right(self):
        self.ang += 20
        self.dx = sin(radians(self.ang))
        self.dy = cos(radians(self.ang))

    def speed_up(self):
        if self.speed < 5:
            self.speed += 1

    def speed_down(self):
        if self.speed >= 0:
            self.speed -= 1

    def move(self):
        if self.size <= self.x <= SCREEN_WIDTH - self.size:
            self.x += self.dx * self.speed
        if self.size <= self.y <= SCREEN_HEIGHT - self.size:
            self.y += self.dy * self.speed

        if self.x < self.size:
            self.x = self.size
        if self.x > SCREEN_WIDTH - self.size:
            self.x = SCREEN_WIDTH - self.size

        if self.y < self.size:
            self.y = self.size
        if self.y > SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size


    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.size, self.size,
                                     [100, 0, 0])
        pass

class Resurse:
    def __init__(self):
        self.size = 50
        self.x = random.randint(self.size, SCREEN_WIDTH - self.size)
        self.y = random.randint(self.size, SCREEN_WIDTH - self.size)
        self.color = [150, 150, 100]
        self.img = arcade.load_texture('img/water.png')

    def draw(self):
        # arcade.draw_rectangle_filled(self.x, self.y, self.size, self.size, self.color)
        arcade.draw_texture_rectangle(self.x, self.y, self.size, self.size, self.img)


class Background:
    def __init__(self):
        self.img = arcade.load_texture("img/background.jpg")

    def draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.img)

class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.AMAZON)
        self.resurse_list = []

    def setup(self):
        # Настроить игру здесь
        self.background = Background()

        self.robot = Robot(100, 250)
        for i in range(RESOURSE_COUNT):
            self.resurse_list.append(Resurse())
        pass

    def draw_telemetry(self):
        telemetry = 'speed: {} \n'.format(self.robot.speed) + \
                    'ang: {} \n'.format(self.robot.ang)

        arcade.draw_text(telemetry, 10, 10, arcade.color.BLACK, 18, anchor_x="left")

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.background.draw()
        for resourse in self.resurse_list:
            resourse.draw()

        self.robot.draw()
        self.draw_telemetry()

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