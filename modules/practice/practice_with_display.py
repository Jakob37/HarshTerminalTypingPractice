import curses
import random
import time
import sys

from colorama import Style, Fore, Back

from modules.utils.getch import _Getch
from modules.practice import practice_visualize_funcs as vis

from modules.practice.book import Book
from modules.utils import log_util

g = _Getch()


def run_practice_with_display(book, auto_return=False, time_limit=None, error_limit=None):

    STATUS_STRING = 'Insert status message here'

    log_util.write_to_log('New run started')

    window = initialize_curses_window()
    run_status = RunStatus(book, time_limit=time_limit, error_limit=error_limit)

    try:
        (h, w) = window.getmaxyx()
        write_center = int(h/2)

        x_margin = 10
        # getch = _Getch()

        vis.visualize(window, write_center, x_margin, run_status, debug_string=STATUS_STRING)

        while not run_status.is_game_over:

            run_status.new_loop()

            new_char = g()
            run_status.check_char(new_char)
            run_status.update_sentence_numbers()

            if run_status.is_sentence_complete() and (run_status.return_struck or auto_return):
                run_status.new_line()

            vis.visualize(window, write_center, x_margin, run_status, debug_string=STATUS_STRING)

            if run_status.limited_run():
                run_status.check_limits()

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

        if run_status.errors == 0:
            text_prefix = 'Really well done, no errors!'
        elif run_status.errors == 1:
            text_prefix = 'Almost there, make it zero errors next time!'
        elif run_status.errors <= 3:
            text_prefix = 'You are getting sloppy, keep track of those fingers!'
        elif run_status.errors <= 5:
            text_prefix = 'Not good, be more careful while typing!'
        elif run_status.errors < 10:
            text_prefix = 'Terrible, start thinking before typing!!'
        else:
            text_prefix = 'So many errors, are you even trying?'

        print('\n{}\nIt took {:.1f} seconds, you made {} errors, wpm: {:.2f}'
            .format(text_prefix, run_status.get_elapsed_time(), run_status.errors, run_status.get_wpm()))


def initialize_curses_window():

    window = curses.initscr()
    curses.start_color()
    curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    return window


class RunStatus:

    def __init__(self, book, time_limit=None, error_limit=None):

        self.book = book

        self.start_time = time.time()
        self.errors = 0
        self.last_wrong = 0
        self.correct = 0
        self.wrong = 0
        self.current_target = self.book.current_line()
        self.current_written = ''
        self.is_game_over = False
        self.return_struck = False

        self.time_limit = time_limit
        self.error_limit = error_limit

    def limited_run(self):
        return self.time_limit is not None or self.error_limit is not None

    def is_sentence_complete(self):
        return self.current_written == self.current_target

    def get_wpm(self):
        return self.book.wpm

    def get_elapsed_time(self):
        return time.time() - self.start_time

    def new_loop(self):
        self.return_struck = False

    def check_limits(self):

        if self.time_limit is not None:
            if self.get_elapsed_time() > self.time_limit:
                self.is_game_over = True

        if self.error_limit is not None:
            if self.errors >= self.error_limit:
                self.is_game_over = True

    def new_line(self):
        self.current_target = self.book.get_next_line()
        self.last_wrong = 0
        self.correct = 0
        self.wrong = 0
        self.current_written = ''

    def check_char(self, new_char):

        if ord(new_char) == 127:   # Backspace
            self.current_written = self.current_written[:-1]
        elif ord(new_char) == 27:  # Escape
            print('\nQuitting...')
            self.is_game_over = True
        elif ord(new_char) == 13:
            self.return_struck = True
        elif len(self.current_written) < len(self.current_target):
            self.current_written += new_char

    def update_sentence_numbers(self):

        correct = 0
        wrong = 0

        target_sent = self.current_target
        actual_sent = self.current_written

        wrong_found = False
        for i in range(len(target_sent)):
            if i < len(actual_sent):
                
                target_letter = target_sent[i]
                actual_letter = actual_sent[i]

                if target_letter == actual_letter and not wrong_found:
                    correct += 1
                else:
                    wrong += 1
                    wrong_found = True
        
        self.correct = correct
        self.wrong = wrong

        if self.wrong > self.last_wrong:
            self.errors += 1
        self.last_wrong = self.wrong
