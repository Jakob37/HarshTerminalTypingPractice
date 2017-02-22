#!/usr/bin/env python3

import colorama
from colorama import Style, Fore, Back
import sys
import time

from modules.utils.getch import _Getch

from modules.practice import practice_with_display

def main(args):

    practice_with_display.run_practice_with_display()

    print('Testing over!')

    sys.exit(1)

    elapsed_time = time.time() - start_time
    score = elapsed_time / (1 + errors)
    print('\nCongratulations, you win! It took {:.1f} seconds, you made {} errors resulting in score {:.1f}'.format(elapsed_time, errors, score))




class Status:

    def __init__(self):
        pass

    def get_elapsed_time(self):
        pass

    def get_score(self):
        pass

    def __str__(self):
        pass
