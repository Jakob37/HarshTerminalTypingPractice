#!/usr/bin/env python3

#import colorama
#from colorama import Style, Fore, Back
import sys
import time

from modules.utils.getch import _Getch

from modules.practice import practice_with_display
from modules.practice.book import Book

def main(args=None):

    if args is None:
        run_test()
    if args.practice_type == 'training':
        run_practice(args)
    elif args.practice_type == 'test':
        run_test(args)
    else:
        print("Not implemented practice type: {}".format(args.practice_type))
        sys.exit(1)


def run_practice(args=None):

    if args is None:
        auto_return = False
    else:
        auto_return = args.auto_return

    book = Book("books/plato_the_republic.txt", rand_start=True)
    practice_with_display.run_practice_with_display(auto_return=auto_return, book=book)


def run_test(args=None):

    time_limit = 60
    error_limit = 15

    if args is None:
        auto_return = False
    else:
        auto_return = args.auto_return


    book = Book("books/plato_the_republic.txt", rand_start=True)
    practice_with_display.run_practice_with_display(auto_return=args.auto_return, 
        book=book,
        time_limit = time_limit,
        error_limit = error_limit)
