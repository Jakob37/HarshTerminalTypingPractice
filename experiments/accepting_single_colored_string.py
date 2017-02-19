#!/usr/bin/env python3

import colorama
import sys
from getch import _Getch



def print_colored_sentence(target_sent, actual_sent):

    correct = 0
    wrong = 0

    for i in range(len(target_sent)):
        if i < len(actual_sent):
            
            target_letter = target_sent[i]
            actual_letter = actual_sent[i]

            if target_letter == actual_letter:
                correct += 1
            else:
                wrong += 1

    print('Correct: {}'.format(target_sent[:correct]))
    print('Wrong: {}'.format(target_sent[correct:wrong]))
    print('Rest: {}'.format(target_sent[wrong:]))



sentence = 'Hello world, and I am writing out this sentence gracefully!'
is_game_over = False
current_sentence = ''
getch = _Getch()

print(sentence)

while not is_game_over:

    new_char = getch()

    if new_char == 'x':
        sys.exit(0)
    elif ord(new_char) == 127:
        current_sentence = current_sentence[:-1]


    current_sentence += new_char
    print_colored_sentence(sentence, current_sentence)












