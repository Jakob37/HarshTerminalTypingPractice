import sqlite3
import datetime
from modules.utils import date_utils

import harty_config

from modules.database import database_interface as db_interface
from modules.book.book_read import BookRead


def add_new_book(name, path):

    conn = db_interface.get_connection()
    cursor = conn.cursor()

    current_date = date_utils.get_current_date_string()
    progress = 0
    spent_time = 0

    params = (name, path, current_date, progress, spent_time)
    command_str = 'INSERT INTO books VALUES (NULL, ?, ?, ?, ?, ?)'

    print(params)

    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def reset_book():
    pass


def update_progress(book, run_status):

    conn = db_interface.get_connection()
    c = conn.cursor()


    conn.close()


def get_books():

    conn = db_interface.get_connection()
    c = conn.cursor()

    c.execute('SELECT * FROM books')
    books = list()
    
    for entry in c:
        book_string = '\t'.join([str(field) for field in entry])
        book_read = BookRead.book_read_from_string(book_string)
        books.append(book_read)
    conn.close()

    return books


def load_book(book_name):

    books = get_books()
    hits = [book_read for book_read in books if book_read.name == book_name]

    if len(hits) != 1:
        raise ValueError('Wrong number of entries found ({}), only one is currently OK'.format(len(hits)))

    target_read = hits[0]
    return target_read


