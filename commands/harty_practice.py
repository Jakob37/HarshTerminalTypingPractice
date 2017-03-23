#!/usr/bin/env python3

import sys
import time

import harty_config

from modules.practice import practice_with_display
from modules.practice.book import Book

REPUBLIC_BOOK = 'plato_the_republic.txt'


def main(args=None):

    if args is None:
        run_test()
    elif args.practice_type == 'training':
        run_practice(args)
    elif args.practice_type == 'test':
        run_test(args)
    else:
        print("Not implemented practice type: {}".format(args.practice_type))
        sys.exit(1)


def test_main(args):

    auto_return = False
    time_limit = 60
    error_limit = 5
    book_path = get_book_path(REPUBLIC_BOOK)
    book = Book(book_path, rand_start=True)
    practice_with_display.run_practice_with_display(auto_return=auto_return,
                                                    book=book,
                                                    is_eval_run=True,
                                                    time_limit=time_limit,
                                                    error_limit=error_limit)


def run_practice(args=None):

    if args is None:
        auto_return = False
    else:
        auto_return = args.auto_return

    description = args.description

    if args.source is None:
        book_path = get_book_path(REPUBLIC_BOOK)
    else:
        book_path = get_book_path(args.source + ".txt")
    book = Book(book_path, rand_start=True)
    practice_with_display.run_practice_with_display(auto_return=auto_return, book=book, descr=description)


def run_test(args=None):

    # if args is None:
    #     auto_return = False
    #     description = 'default test'
    # else:
    #     auto_return = args.auto_return
    #     description = args.description

    conf = harty_config.get_config()
    time_limit = conf.getint('settings', 'time_threshold')
    error_limit = conf.getint('settings', 'error_threshold')

    book_path = get_book_path(REPUBLIC_BOOK)
    book = Book(book_path, rand_start=True)
    description = 'TEST_EVAL'
    practice_with_display.run_practice_with_display(book=book,
                                                    time_limit=time_limit,
                                                    error_limit=error_limit,
                                                    descr=description)


def get_book_path(book_file_name):

    conf = harty_config.get_config()
    book_base = conf.get('file_paths', 'book_base')
    return '{}/{}'.format(book_base, book_file_name)
