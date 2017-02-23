import curses
import random
import time
import sys

from colorama import Style, Fore, Back

from modules.utils.getch import _Getch
from modules.practice import practice_visualize_funcs as vis

from modules.practice.book import Book

g = _Getch()


def run_practice_with_display():

    window = curses.initscr()
    curses.start_color()
    curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)

    test_book = Book("books/plato_the_republic.txt")
    sentence = test_book.get_next_line()

    start_time = time.time()
    errors = 0
    last_wrong = 0
    correct = 0
    wrong = 0

    try:
        (h, w) = window.getmaxyx()

        write_center = int(h/2)
        x_margin = 10

        # print('Height: {} Width: {}'.format(window.getmaxyx()[0],window.getmaxyx()[1]))

        # sentence = 'Hello world, and I am writing out this sentence gracefully!'
        is_game_over = False
        current_sentence = ''
        getch = _Getch()

        vis.visualize(window, write_center, x_margin, sentence, correct, wrong, errors, start_time)

        while not is_game_over:

            new_char = g()

            if ord(new_char) == 127:   # Backspace
                current_sentence = current_sentence[:-1]
            elif ord(new_char) == 27:  # Escape
                print('\nQuitting...')
                is_game_over = True
            else:
                current_sentence += new_char

            correct, wrong = get_sentence_numbers(sentence, current_sentence)

            if wrong > last_wrong:
                errors += 1
            last_wrong = wrong

            vis.visualize(window, write_center, x_margin, sentence, correct, wrong, errors, start_time)

            if current_sentence == sentence:
                # is_game_over = True
                sentence = test_book.get_next_line()
                errors = 0
                last_wrong = 0
                correct = 0
                wrong = 0
                current_sentence = ''


    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

        elapsed_seconds = time.time() - start_time

        words = len(sentence.split(' '))
        wpm = words / (elapsed_seconds / 60)

        score = elapsed_seconds / (1 + errors)
        print('\nCongratulations, you win! It took {:.1f} seconds, you made {} errors, wpm: {:.2f}, score {:.1f}'.format(elapsed_seconds, errors, wpm, score))



def get_sentence_numbers(target_sent, actual_sent):

    correct = 0
    wrong = 0

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
    return (correct, wrong)


