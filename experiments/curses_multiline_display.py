#!/usr/bin/env python3

# from curses import wrapper

# Taken from: https://docs.python.org/3/howto/curses.html

# def main(stdscr):
# 	stdscr.clear()

# 	for i in range(1, 11):
# 		v = i - 10
# 		stdscr.addstr(i, 0, '10 times {} is {}'.format(v, 10 * v))

# 	stdscr.refresh()
# 	stdscr.getkey()

# wrapper(main)


# import curses
# from curses import wrapper
# from curses.textpad import Textbox, rectangle

# def main(stdscr):
#     stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

#     editwin = curses.newwin(5,30, 2,1)
#     rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
#     stdscr.refresh()

#     box = Textbox(editwin)

#     # Let the user edit until Ctrl-G is struck.
#     box.edit()

#     # Get resulting contents
#     message = box.gather()

#     print("HI")


# wrapper(main)

import curses
import random
import time
import sys

from getch import _Getch

g = _Getch()

window = curses.initscr()

try:
    (h, w) = window.getmaxyx()

    print('Height: {} Width: {}'.format(window.getmaxyx()[0],window.getmaxyx()[1]))

    while True:
        x = int(random.random() * w)
        y = int(random.random() * h)
        window.move(y, x)

        new_char = g()

        if ord(new_char) == 27:  # Escape
            print('\nQuitting game...')
            sys.exit(0)

        window.addch(new_char)
        window.refresh()
        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    curses.endwin()