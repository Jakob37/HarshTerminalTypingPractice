import curses
import random
import time
import sys

from colorama import Style, Fore, Back

from modules.utils.getch import _Getch

g = _Getch()


def run_practice_with_display():

    window = curses.initscr()
    curses.start_color()
    curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)

    try:
        (h, w) = window.getmaxyx()

        write_center = int(h/2)
        x_margin = 10

        # print('Height: {} Width: {}'.format(window.getmaxyx()[0],window.getmaxyx()[1]))

        sentence = 'Hello world, and I am writing out this sentence gracefully!'
        is_game_over = False
        current_sentence = ''
        getch = _Getch()
        start_time = time.time()

        errors = 0
        last_wrong = 0


        window.refresh()
        while not is_game_over:
            # x = int(random.random() * w)
            # y = int(random.random() * h)
            # window.move(0, 0)

            new_char = g()

            if ord(new_char) == 127:   # Backspace
                current_sentence = current_sentence[:-1]
            elif ord(new_char) == 27:  # Escape
                print('\nQuitting game...')
                sys.exit(0)
            else:
                current_sentence += new_char

            if ord(new_char) == 27:  # Escape
                print('\nQuitting...')
                return

            correct, wrong = get_sentence_numbers(sentence, current_sentence)

            if wrong > last_wrong:
                errors += 1
            last_wrong = wrong


            visualize(window, write_center, x_margin, sentence, correct, wrong, errors, start_time)

            if current_sentence == sentence:
                is_game_over = True


            # window.addch(new_char)
            # time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
        print('end after')

    print("outside")



def visualize(window, write_center, x_margin, sentence, correct, wrong, errors, start_time):
    window.clear()

    # colored_sentence = get_colored_sentence(sentence, correct, wrong)
    status_sentence = get_status_string(start_time, correct, errors)

    # print('{}\n{}'.format(status_sentence, colored_sentence), end='\r')

    # curses.start_color()

    window.addstr(write_center - 2, x_margin, "statusstr", curses.color_pair(curses.COLOR_GREEN))
    window.addstr(write_center + 2, x_margin, status_sentence)
    write_colored_sentence(window, x_margin, write_center + 3, sentence, correct, wrong)
    # window.addstr(write_center + 3, x_margin, colored_sentence)

    window.refresh()


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


def write_colored_sentence(window, x, y, target_sent, correct, wrong):

    corr_str = target_sent[:correct]
    wrong_str = target_sent[correct:correct+wrong]
    rest = target_sent[correct+wrong:]

    window.addstr(y, x, corr_str, curses.color_pair(curses.COLOR_GREEN))
    window.addstr(y, x + len(corr_str), wrong_str, curses.color_pair(curses.COLOR_RED))
    window.addstr(y, x + len(corr_str) + len(wrong_str), rest)


def get_status_string(start_time, correct, wrong):

    elapsed_time = time.time() - start_time
    return '{} seconds, {} correct, {} errors'.format(int(elapsed_time), correct, wrong)
