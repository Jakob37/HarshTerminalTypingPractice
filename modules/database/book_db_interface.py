import sqlite3
import datetime
from modules.utils import date_utils

import harty_config

from modules.database import database_interface as db_interface


def add_new_book(name, path):

    conn = db_interface.get_connection()
    cursor = conn.cursor()

    current_date = date_utils.get_current_date_string()
    progress = 0
    spent_time = 0

    params = (name, path, current_date, progress, spent_time)
    command_str = 'INSERT INTO books VALUES (NULL, ?, ?, ?, ?, ?)'
    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def reset_book():
    pass


def update_progress(book, run_status):
    pass


def load_progress(book):
    pass

