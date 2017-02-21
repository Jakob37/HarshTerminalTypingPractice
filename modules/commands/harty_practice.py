#!/usr/bin/env python3

import colorama
from colorama import Style, Fore, Back
import sys
import time

from modules.utils.getch import _Getch

def main(args):

    sentence = 'Hello world, and I am writing out this sentence gracefully!'
    is_game_over = False
    current_sentence = ''
    getch = _Getch()
    start_time = time.time()

    errors = 0
    last_wrong = 0

    print('Welcome! Escape to quit. Type out the sentence below.\n')
    print(sentence, end='\r')

    while not is_game_over:

        new_char = getch()

        if ord(new_char) == 127:  # Backspace
            current_sentence = current_sentence[:-1]
        elif ord(new_char) == 27:  # Escape
            print('\nQuitting game...')
            sys.exit(0)
        else:
            current_sentence += new_char


        correct, wrong = get_sentence_numbers(sentence, current_sentence)

        if wrong > last_wrong:
            errors += 1
        last_wrong = wrong

        colored_sentence = get_colored_sentence(sentence, correct, wrong)
        status_sentence = get_status_string(start_time, correct, errors)

        print('{}\n{}'.format(status_sentence, colored_sentence), end='\r')

        if current_sentence == sentence:
            is_game_over = True


    elapsed_time = time.time() - start_time
    score = elapsed_time / (1 + errors)
    print('\nCongratulations, you win! It took {:.1f} seconds, you made {} errors resulting in score {:.1f}'.format(elapsed_time, errors, score))


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


def get_colored_sentence(target_sent, correct, wrong):

    corr_str = target_sent[:correct]
    wrong_str = target_sent[correct:correct+wrong]
    rest = target_sent[correct+wrong:]

    print_str = '{col_green}{corr_str}{col_red}{wrong_str}{col_reset}{rest_str}'
    colored_str = print_str.format(col_green=Fore.GREEN,
                                   col_red=Fore.RED,
                                   col_reset=Style.RESET_ALL,
                                   corr_str=corr_str,
                                   wrong_str=wrong_str,
                                   rest_str=rest)
    return colored_str


def get_status_string(start_time, correct, wrong):

    elapsed_time = time.time() - start_time
    return '{} seconds, {} correct, {} errors'.format(int(elapsed_time), correct, wrong)


class Status:

    def __init__(self):
        pass

    def get_elapsed_time(self):
        pass

    def get_score(self):
        pass

    def __str__(self):
        pass
