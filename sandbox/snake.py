"""
Snakes Curser based game
from https://www.youtube.com/watch?v=rbasThWVb-c
"""
import random
import cursers

s = cursers.initscr()
cursers.curs_set(0)
sh, sw = s.getmaxyx()
w = cursers.newmin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

snk_x = sw/4
snk_y = sh/2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

food = [sh/2, sw/2]
w.addch(food[0], food[1], curses.ACS_PI)

key = cursers.KEY_RIGHT
# main loop
while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
        cursers.endwin()
        quit()

    new_head = [snake[0][0], snake[0][1]]

    if key == cursers.KEY_DOWN:
        new_head[0] += 1
    if key == cursers.KEY_UP:
        new_head[0] -= 1
    if key == cursers.KEY_LEFT:
        new_head[1] -= 1
    if key == cursers.KEY_RIGHT:
        new_head[1] += 1

    snake.insert(0, new_head)
    if snake[0] == food:
        food = None
        while food is None:
            new_food = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = new_food if new_food not in snake else None
        w.addch(food[0], food[1], cursers.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    w.addch(snake[0][0], snake[0],[1], curses.ACS_CKBOARD)
