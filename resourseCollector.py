import arcade
import random
from math import sin, cos, radians

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RESOURSE_COUNT = 9

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
        self.speed = 0
        self.speed_turn = 0
        self.ang = 0
        self.dx = sin(radians(self.ang))
        self.dy = cos(radians(self.ang))
        self.fuel = 100
        self.fuel_dec = 0.1
        self.size = 60
        self.box_total = 4
        self.box_current = 0
        self.img = arcade.load_texture('img/robot1.png')
        self.color = arcade.color.BLOND

    def turn_left(self):
        self.speed_turn = -1

    def turn_right(self):
        self.speed_turn = 1

    def turn_stop(self):
        self.speed_turn = 0

    def speed_up(self):
        if self.speed < 5:
            self.speed += 0.5

    def speed_down(self):
        if self.speed >= 0:
            self.speed -= 0.5

    def load_box(self):
        if self.box_current < self.box_total:
            self.box_current += 1
            return True

    def unload_box(self):
        box_count = self.box_current
        self.box_current = 0
        return box_count

    def move(self):
        if self.fuel > 0:
            self.fuel -= self.fuel_dec * (abs(self.speed) * 0.3)
            if self.size / 2 <= self.x <= SCREEN_WIDTH - self.size / 2 and \
               self.size / 2 <= self.y <= SCREEN_HEIGHT - self.size / 2:
                self.x += self.dx * self.speed
                self.y += self.dy * self.speed
            else:
                if self.x < self.size / 2:
                    self.x = self.size / 2
                if self.x > SCREEN_WIDTH - self.size / 2:
                    self.x = SCREEN_WIDTH - self.size / 2

                if self.y < self.size / 2:
                    self.y = self.size / 2
                if self.y > SCREEN_HEIGHT - self.size / 2:
                    self.y = SCREEN_HEIGHT - self.size / 2

    def update(self):
        self.ang += self.speed_turn
        self.dx = sin(radians(self.ang))
        self.dy = cos(radians(self.ang))
        if self.ang < 0:
            self.ang += 360
        self.ang %= 360
        if self.speed_turn != 0:
            self.fuel -= self.fuel_dec * (abs(self.speed_turn) * 0.1)

    def draw(self):
        # arcade.draw_rectangle_filled(self.x, self.y, self.size, self.size, [100, 0, 0])
        arcade.draw_texture_rectangle(self.x, self.y, self.size, self.size, self.img, 360 - self.ang)
        pass


class Resurse:
    type_list = ['water', 'stone', 'iron']
    def __init__(self):
        self.type = random.choice(Resurse.type_list)
        self.size = 50
        self.x = random.randint(self.size, SCREEN_WIDTH - self.size)
        self.y = random.randint(self.size, SCREEN_HEIGHT - self.size)
        self.color = [150, 150, 100]
        if self.type == 'water':
            self.img = arcade.load_texture('img/res_water.png')
        elif self.type == 'stone':
            self.img = arcade.load_texture('img/res_stone.png')
        elif self.type == 'iron':
            self.img = arcade.load_texture('img/res_metal.png')

    def draw(self):
        # arcade.draw_rectangle_filled(self.x, self.y, self.size, self.size, self.color)
        arcade.draw_texture_rectangle(self.x, self.y, self.size, self.size, self.img)


class Base:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = 50
        self.size = 150
        self.resourses_max = 10
        self.resourses = 0
        self.img = arcade.load_texture("img/base.png")

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, self.size, self.size, self.img)
        size_x = 20
        size_y = self.size / self.resourses_max
        for i in range(self.resourses_max):
            x = self.x + self.size * 0.5
            y = 10 + size_y * i
            if i < self.resourses:
                color = arcade.color.GREEN
            else:
                color = arcade.color.GRAY
            arcade.draw_rectangle_filled(x, y, size_x, size_y - 1, color)

    def load_box(self, box_count):
        # загружаем коробки с ресурсами на базу. Лишние исчезают.
        self.resourses += box_count
        self.resourses %= self.resourses_max


class Background:
    def __init__(self):
        self.img = arcade.load_texture("img/background.png")

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
        self.state = 'run'
        self.background = Background()
        self.base = Base()
        self.robot = Robot(self.base.x, self.base.y + 50)
        for i in range(RESOURSE_COUNT):
            self.resurse_list.append(Resurse())

    def draw_telemetry(self):
        telemetry = 'скорость: {} \n'.format(self.robot.speed) + \
                    'топливо: {} %\n'.format(round(self.robot.fuel)) + \
                    'в поле: {} \n'.format(len(self.resurse_list)) + \
                    'на борту: {} \n'.format(self.robot.box_current)

        arcade.draw_xywh_rectangle_filled(5, 10, 150, 120, arcade.color.DARK_BLUE_GRAY)
        arcade.draw_xywh_rectangle_outline(5, 10, 150, 120, arcade.color.BLACK, 4)
        arcade.draw_text(telemetry, 10, 100, arcade.color.YELLOW, 15, anchor_x="left")


    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.background.draw()
        self.base.draw()
        for resourse in self.resurse_list:
            resourse.draw()
        self.robot.draw()
        self.draw_telemetry()
        if self.state == 'game_over':
            arcade.draw_text("Миссия провалена!",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.RED, 30, width=500,
                             align="center", anchor_x="center", anchor_y="center")
        if self.state == 'win':
            arcade.draw_text("УРА!!!\nМиссия выполнена!\nвсе ресурсы доставлены на базу",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.RED, 25, width=500,
                             align="center", anchor_x="center", anchor_y="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
             self.robot.turn_left()
        if symbol == arcade.key.RIGHT:
             self.robot.turn_right()
        if symbol == arcade.key.UP:
             self.robot.speed_up()
        if symbol == arcade.key.DOWN:
             self.robot.speed_down()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
             self.robot.turn_stop()
        if symbol == arcade.key.RIGHT:
            self.robot.turn_stop()

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        if self.state == 'run':
            self.robot.update()
            self.robot.move()
            for resourse in self.resurse_list:
                if check_collision(resourse, self.robot):
                    if self.robot.load_box():
                        self.resurse_list.remove(resourse)

            if check_collision(self.base, self.robot):
                self.base.load_box(self.robot.unload_box())

            if self.robot.fuel <= 0:
                self.state = 'game_over'
            elif len(self.resurse_list) == 0 and self.robot.box_current == 0:
                self.state = 'win'


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()