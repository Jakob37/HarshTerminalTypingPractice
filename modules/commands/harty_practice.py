#!/usr/bin/env python3

import colorama
from colorama import Style, Fore, Back
import sys
import time

from modules.utils.getch import _Getch

from modules.practice import practice_with_display
from modules.practice.book import Book

def main(args):

    if args.practice_type == 'training':
        run_practice(args)
    elif args.practice_type == 'test':
        run_test(args)
    else:
        print("Not implemented practice type: {}".format(args.practice_type))
        sys.exit(1)



def run_practice(args):

    book = Book("books/plato_the_republic.txt", rand_start=True)

    practice_with_display.run_practice_with_display(auto_return=args.auto_return, book=book)


def run_test(args):
    print('run test')