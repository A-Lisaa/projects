import turtle
import random
import math
from typing import Iterable


# Параметры
SCREEN_SIZE: tuple[int, int] = (1600, 900) # Размеры окна
BG_COLOR: str = "#00BFFF" # Цвет фона
START_POS: tuple[float, float] = (0, 350) # Начальная позиция черепашки
START_LENGTH: float = 50 # Длина первой ветки
END_LENGTH: float = 250 # Длина последней ветки
STEP_LENGTH: float = 10 # Увеличение длины каждой ветки
SPACE_LENGTH: float = 20 # Расстояние между ветками
BALL_CHANCE: float = 0.1 # Шанс появления шарика для каждого пикселя, если не будет пересечения с другим
BALL_SIZES: tuple[int, int] = (8, 13) # Размер шара от a до b
ANGLE: float = 45 # Угол веток от ствола налево
AMOUNT_OF_SNOWFLAKES: int = 1000 # Кол-во снежинок
SNOWFLAKE_SIZES: tuple[int, int] = (7, 10) # Размер снежинок от a до b

MAGIC_NUMBER: float = 28 # Магическое число для нижних веток, ебу как получить (возможно, как-то связано с углом)
balls = []
t = turtle.Turtle()
s = turtle.Screen()

def draw_init():
    s.bgcolor(BG_COLOR)
    s.setup(SCREEN_SIZE[0], SCREEN_SIZE[1])
    #t.hideturtle()
    t.speed("fastest")

def draw_shaft():
    #t.up()
    t.pensize(10)
    t.pencolor("brown")
    # SPACE_LENGTH + 6 might not work, figure out the number (foemula)
    t.goto(START_POS[0], START_POS[1] - ((END_LENGTH - START_LENGTH)/STEP_LENGTH * (SPACE_LENGTH + 7)))
    t.goto(START_POS)
    t.pencolor("green")
    t.pensize(4)

def draw_branches(iter: Iterable, angle: float):
    for length in iter:
        t.down()
        t.right(angle)
        t.fd(length)
        #t.dot(10, "yellow" if iter.step == STEP_LENGTH else "red")
        t.bk(length)
        t.left(angle)
        # Rewrite w\o t.up() and t.down()
        t.up()
        t.fd(SPACE_LENGTH)

def draw_toys(iter: Iterable, angle: float, y_shift: float):
    for length in iter:
        max_x = -int(math.sin(math.radians(angle))*length)
        for x in range(max_x, 0, 1 if max_x < 0 else -1):
            if random.random() < BALL_CHANCE:
                t.goto(x, math.tan(math.radians(90 - angle))*x + y_shift)

                no_intersection = True
                x_pos, y_pos = t.pos()
                for (x_ball, y_ball), ball_size in balls:
                    center_dist = math.sqrt((x_pos-x_ball)*(x_pos-x_ball) + (y_pos-y_ball)*(y_pos-y_ball))
                    if center_dist <= 2*ball_size:
                        no_intersection = False

                if no_intersection:
                    ball_size = random.randint(BALL_SIZES[0], BALL_SIZES[1])
                    balls.append((t.pos(), ball_size))
                    color = (random.randint(0, 255)/255,
                             random.randint(0, 255)/255,
                             random.randint(0, 255)/255)
                    t.dot(ball_size, color)
        y_shift -= SPACE_LENGTH

    return y_shift

def draw_snowflakes():
    for _ in range(AMOUNT_OF_SNOWFLAKES):
        pos = (random.randint(int(-s.window_width()/2), int(s.window_width()/2)),
            random.randint(int(-s.window_height()/2), int(s.window_height()/2)))
        t.goto(pos)
        size = random.randint(SNOWFLAKE_SIZES[0], SNOWFLAKE_SIZES[1])
        t.dot(size, (1, 1, 1))

def draw_branch_side(angle: float):
    t.setheading(270)
    t.goto(START_POS)

    normal_rng = range(START_LENGTH, END_LENGTH, STEP_LENGTH)
    backward_rng = range(END_LENGTH, START_LENGTH, int(-STEP_LENGTH*(MAGIC_NUMBER/STEP_LENGTH)))

    draw_branches(normal_rng, angle)
    draw_branches(backward_rng, angle)

def draw_toy_side(angle: float):
    normal_rng = range(START_LENGTH, END_LENGTH, STEP_LENGTH)
    backward_rng = range(END_LENGTH, START_LENGTH, int(-STEP_LENGTH*(MAGIC_NUMBER/STEP_LENGTH)))

    t.up()
    t.goto(START_POS)
    y_shift = draw_toys(normal_rng, angle, START_POS[1])
    draw_toys(backward_rng, angle, y_shift)

def draw_sides(angle: float):
    draw_init()
    t.pensize(4)
    draw_shaft()
    draw_branch_side(angle)
    draw_branch_side(-angle)
    #draw_toy_side(angle)
    #draw_toy_side(-angle)

if __name__ == "__main__":
    draw_sides(ANGLE)
    draw_snowflakes()
    s.exitonclick()
