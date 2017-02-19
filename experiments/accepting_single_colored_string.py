#!/usr/bin/env python3

import colorama
from colorama import Style, Fore, Back
import sys
import time

from getch import _Getch



def print_colored_sentence(target_sent, actual_sent):

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

    print(colored_str, end='\r')


sentence = 'Hello world, and I am writing out this sentence gracefully!'
is_game_over = False
current_sentence = ''
getch = _Getch()
start_time = time.time()

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

    print_colored_sentence(sentence, current_sentence)

    if current_sentence == sentence:
        is_game_over = True


elapsed_time = time.time() - start_time


print('\nCongratulations, you win! It tool {:.2f} seconds'.format(elapsed_time))







