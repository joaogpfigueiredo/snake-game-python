import time
import random
import functools
import turtle
from pathlib import Path

MAX_X = 600
MAX_Y = 760
DEFAULT_SIZE = 20
velocity = 0.1
level_count = 0
SNAKE_SHAPE = 'square'
DIR_PATH = Path(__file__).parent
HIGH_SCORES_FILE_PATH = DIR_PATH.joinpath("high_scores.txt")
EXIT_FILE_PATH = DIR_PATH.joinpath("Exit.gif")
turtle.register_shape(str(EXIT_FILE_PATH))


def load_high_score(state):
    with open(HIGH_SCORES_FILE_PATH) as high_scores:
        last_line = high_scores.readlines()
        if len(last_line) > 0:
            if len(last_line) == 1:
                last_line = last_line[0]
            else:
                last_line = last_line[-1]
            h_score = ""
            for i in last_line:
                if i.isnumeric():
                    h_score = h_score + str(i)
            state['high_score'] = int(h_score)
            state['last_high_score'] = state['high_score']


def write_high_score_to_file(state):
    if state['high_score'] != 0:
        with open(HIGH_SCORES_FILE_PATH, "a") as high_scores:
            high_scores.write("New High Score: {}\n".format(state['high_score']))


def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("black")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(-MAX_X / 2.55, MAX_Y / 2.27)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)


def update_score_board(state):
    state['score_board'].clear()
    if state['last_high_score'] < state['score']:
        state['new_high_score'] = True
        state['level_count'] += 1
    if state['score'] >= state['high_score']:
        state['high_score'] = state['score']
    state['score_board'].write("Score: {} \nHigh Score: {}".format(state['score'], state['high_score']), align="center",
                               font=("Helvetica", 15, "normal"))


def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'


def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'


def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'


def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'


def init_state():
    state = {}
    # Informação necessária para a criação do score board
    state['score_board'] = None
    state['new_high_score'] = False
    state['last_high_score'] = 0
    state['high_score'] = 0
    state['score'] = 0
    # Para gerar a comida deverá criar um nova tartaruga e colocar a mesma numa posição aleatória do campo
    state['food'] = None
    state['window'] = None
    # Para a dificuldade do jogo
    state['difficulty'] = None
    state['level_count'] = 0
    snake = {
        'head': None,  # Variável que corresponde à cabeça da cobra
        'current_direction': None,  # Indicação da direcção atual do movimento da cobra
        'tail': []
    }
    state['snake'] = snake
    return state


def area():
    campo = turtle.Turtle()
    campo.hideturtle()
    campo.pu()
    campo.goto(-MAX_X // 2.04, -MAX_Y // 2.06)
    campo.pd()
    for i in range(2):
        campo.fd(MAX_X // 1.025)
        campo.left(90)
        campo.fd(MAX_Y // 1.08)
        campo.left(90)


def setup(state):
    if not HIGH_SCORES_FILE_PATH.is_file():
        open(HIGH_SCORES_FILE_PATH, "x")
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    keys = [['w', 'W', 'Up'], ['s', 'S', 'Down'], ['a', 'A', 'Left'], ['d', 'D', 'Right']]
    for key in range(len(keys)):
        for orientation in range(3):
            if key == 0:
                window.onkey(functools.partial(go_up, state), keys[key][orientation])
            elif key == 1:
                window.onkey(functools.partial(go_down, state), keys[key][orientation])
            elif key == 2:
                window.onkey(functools.partial(go_left, state), keys[key][orientation])
            else:
                window.onkey(functools.partial(go_right, state), keys[key][orientation])
    window.tracer(0)
    area()
    state['window'] = window
    state['difficulty'] = turtle.Turtle()
    state['difficulty'].pu()
    state['difficulty'].hideturtle()
    state['difficulty'].goto(-MAX_X // 2.33, -MAX_Y // 2.07)
    state['difficulty'].write("Difficulty 0", align="center", font=("Helvetica", 11, "normal"))
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('green')
    create_score_board(state)
    create_food(state)


def move(state):
    snake = state['snake']  # Dicionário da snake
    head = snake['head']  # Cabeça da cobra
    if snake['current_direction'] == 'up':
        head.setheading(90)  # Fazer com que a cobra se movimente para cima após pressionar w!
    elif snake['current_direction'] == 'down':
        head.setheading(270)  # Fazer com que a cobra se movimente para baixo após pressionar s!
    elif snake['current_direction'] == 'right':
        head.setheading(0)  # Fazer com que a cobra se movimente para direita após pressionar d!
    elif snake['current_direction'] == 'left':
        head.setheading(180)  # Fazer com que a cobra se movimente para esquerda após pressionar a!
    if snake['current_direction'] != 'stop':
        head.forward(20)  # Andar 20 pixeis na direção que lhe foi atribuida!


def create_food(state):
    x = random.randint(int(-MAX_X // 2.15), int(MAX_X // 2.2))
    y = random.randint(int(-MAX_Y // 2.15), int(MAX_Y // 2.4))
    state['food'] = turtle.Turtle()
    state['food'].shape("circle")
    state['food'].color("red")
    state['food'].shapesize(0.5)
    state['food'].pu()
    state['food'].hideturtle()
    state['food'].goto(x, y)
    state['food'].showturtle()


def check_if_food_to_eat(state):
    food = state['food']
    head = state['snake']['head']
    tail = state['snake']['tail']
    if head.distance(food) <= 15:
        food.hideturtle()
        cauda = turtle.Turtle()
        cauda.shape(SNAKE_SHAPE)
        cauda.color("black")
        cauda.pu()
        tail.append(cauda)
        state['score'] = state['score'] + 10
        update_score_board(state)
        create_food(state)


def boundaries_collision(state):
    x = state['snake']['head'].xcor()
    y = state['snake']['head'].ycor()
    if (x >= MAX_X // 2.04) or (x <= -(MAX_X // 2.04)) or (y >= MAX_Y // 2.25) or (y <= -(MAX_Y // 2.06)):
        return True
    else:
        return False


def check_collisions(state):
    tail = state['snake']['tail']
    head = state['snake']['head']
    if len(tail) < 3:
        return boundaries_collision(state)
    else:
        for i in range(len(tail) - 1, 0, -1):
            if tail[i].distance(head) < 15:
                return True
    return boundaries_collision(state)


def leave_button(state):
    def button(x, y):
        if state['new_high_score']:
            write_high_score_to_file(state)
        turtle.Screen().bye()
    leave = turtle.Turtle()
    leave.pu()
    leave.shape(str(EXIT_FILE_PATH))
    leave.goto(MAX_X / 2.4, MAX_Y / 2.13)
    leave.onclick(button)


def restart():
    global velocity
    time.sleep(1)
    turtle.clearscreen()
    velocity = 0.1
    r = turtle.Turtle()
    r.hideturtle()
    r.write("Restarting The Game ...", align="center", font=("Helvetica", 24, "normal"))
    time.sleep(1)
    turtle.clearscreen()


def difficulty(state):
    global velocity
    global level_count
    if state['level_count'] == 5:
        state['level_count'] = 0
        level_count += 1
        state['difficulty'].clear()
        if velocity != 0.05:
            velocity -= 0.01
            state['difficulty'].write("Difficulty {}".format(level_count), align="center", font=("Helvetica", 11, "normal"))
        else:
            state['difficulty'].write("Difficulty MAX", align="center", font=("Helvetica", 11, "normal"))


def main():
    state = init_state()
    setup(state)
    leave_button(state)
    tail = state['snake']['tail']
    head = state['snake']['head']
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        for i in range(len(tail) - 1, 0, -1):
            tail[i].goto(tail[i - 1].xcor(), tail[i - 1].ycor())
        if len(tail) > 0:
            tail[0].goto(head.xcor(), head.ycor())
        difficulty(state)
        move(state)
        time.sleep(velocity)
    if state['new_high_score']:
        write_high_score_to_file(state)
    restart()
    main()


main()
