import curses
import random
import time
import sys

from colorama import Style, Fore, Back

from modules.utils.getch import _Getch
from modules.practice import practice_visualize_funcs as vis

from modules.practice.book import Book

g = _Getch()


DEBUG = False



def run_practice_with_display(book, auto_return=False):

    STATUS_STRING = 'Insert status message here'

    if not DEBUG:
        window = curses.initscr()
        curses.start_color()
        curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)

    run_status = RunStatus(book)

    try:
        if not DEBUG:
            (h, w) = window.getmaxyx()
            write_center = int(h/2)

        x_margin = 10
        getch = _Getch()

        if not DEBUG:
            vis.visualize(window, write_center, x_margin, run_status, debug_string=STATUS_STRING)
        else:
            print(current_sentence + " " + sentence)
            print('Length curr: {} length tot: {}'.format(len(current_sentence), len(sentence)))


        while not run_status.is_game_over:

            run_status.new_loop()

            new_char = g()
            run_status.check_char(new_char)
            run_status.update_sentence_numbers()

            if run_status.is_sentence_complete() and (run_status.return_struck or auto_return):
                run_status.new_line()

            if not DEBUG:

                vis.visualize(window, write_center, x_margin, run_status, debug_string=STATUS_STRING)
            else:
                print('{!r} {!r}'.format(current_sentence, sentence))
                print('Length curr: {} length tot: {}'.format(len(current_sentence), len(sentence)))


    except KeyboardInterrupt:
        pass
    finally:
        if not DEBUG:
            curses.endwin()

        elapsed_seconds = time.time() - run_status.start_time

        print('\nCongratulations, you win! It took {:.1f} seconds, you made {} errors, wpm: {:.2f}'
            .format(elapsed_seconds, run_status.errors, run_status.get_wpm()))



class RunStatus:

    def __init__(self, book):

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


    def is_sentence_complete(self):
        return self.current_written == self.current_target

    def get_wpm(self):
        return self.book.wpm


    def new_loop(self):
        self.return_struck = False

    def new_line(self):
        sentence = self.book.get_next_line()
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
