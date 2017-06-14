import sqlite3

import harty_config

from modules.utils import date_utils
from modules.practice.run_status import RunStatus

ENTRY_TABLE = 'type_entries'

ENTRY_FIELDS = [('entry_id', 'INTEGER PRIMARY KEY'),
                ('date_stamp', 'TEXT'),
                ('time_stamp', 'TEXT'),
                ('typed_characters', 'INTEGER'),
                ('wpm', 'NUMERIC'),
                ('completed', 'BIT'),
                ('total_time_seconds', 'INTEGER'),
                ('total_typed_characters', 'INTEGER'),
                ('total_errors', 'INTEGER'),
                ('type_stamp', 'TEXT'),
                ('description', 'TEXT')]


BOOK_TABLE = 'books'

BOOK_FIELDS = [('entry_id', 'INTEGER PRIMARY KEY'),
               ('name', 'TEXT'),
               ('path', 'TEXT'),
               ('date_create', 'TEXT'),
               ('progress', 'INTEGER'),
               ('spent_time', 'NUMERIC')]


def setup_database(database_path, dry_run=False):

    print('Attempting to open database at: {}'.format(database_path))

    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    create_entry_table = get_create_table_command(ENTRY_TABLE, ENTRY_FIELDS)
    c.execute(create_entry_table)

    create_entry_table = get_create_table_command(BOOK_TABLE, BOOK_FIELDS)
    c.execute(create_entry_table)

    if not dry_run:
        conn.commit()
    else:
        print("Dry run, changes not committed")

    conn.close()


def get_connection():

    conf = harty_config.get_config()
    db_path = conf.get('file_paths', 'sql_path')

    conn = sqlite3.connect(db_path)
    return conn


def close_connection(conn, commit_changes):

    if commit_changes:
        conn.commit()

    conn.close()


def get_create_table_command(table_name, field_tuples):

    """
    Expects an open SQLite cursor, table name and a list of name/type tuples
    Valid SQLite types are:

    INTEGER, REAL, TEXT, BLOB, NULL
    """

    database_str = 'CREATE TABLE {name} ({fields})'

    field_strings = ['{} {}'.format(field[0], field[1]) for field in field_tuples]
    field_str = ', '.join(field_strings)

    return database_str.format(name=table_name, fields=field_str)


def write_run_entry(run_entry, verbose=False):

    conn = get_connection()
    cursor = conn.cursor()

    current_date = date_utils.get_current_date_string()
    current_time = date_utils.get_current_time_string()

    if run_entry.is_eval_run:
        type_stamp_text = 'EVAL'
    elif run_entry.description == 'TEST_EVAL':
        type_stamp_text = 'TEST_EVAL'
    else:
        type_stamp_text = 'unspecified'

    print('Is completed: {}'.format(run_entry.is_completed(as_digit=True)))

# ENTRY_FIELDS = [('entry_id', 'INTEGER PRIMARY KEY'),
#                 ('date_stamp', 'TEXT'),
#                 ('time_stamp', 'TEXT'),
#                 ('typed_characters', 'INTEGER'),
#                 ('wpm', 'NUMERIC'),
#                 ('completed', 'BIT'),
#                 ('total_time_seconds', 'INTEGER'),
#                 ('total_typed_characters', 'INTEGER'),
#                 ('total_errors', 'INTEGER'),
#                 ('type_stamp', 'TEXT'),
#                 ('description', 'TEXT')]

    params = (current_date,
              current_time,
              run_entry.get_total_correct(),
              run_entry.get_wpm(),
              run_entry.is_completed(as_digit=True),
              run_entry.time_limit,
              run_entry.get_total_correct(),
              run_entry.errors,
              type_stamp_text,
              run_entry.description)
    command_str = 'INSERT INTO {table_name} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(table_name=ENTRY_TABLE)

    if verbose:
        print("Command to be executed: '{}'".format(command_str))

    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def list_entries_in_table(cursor, table_name):

    for row in cursor.execute('SELECT * FROM {}'.format(table_name)):
        string_values = [str(val) for val in row]
        print('\t'.join(string_values))


def get_run_entry_dicts(sep='\t'):

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM type_entries')
    time_entry_strings = sql_tuples_to_delimited_strings(c.fetchall(), delim=sep)
    conn.close()

    run_status_entries = list()
    for entry_string in time_entry_strings:
        run_status_entries.append(RunStatus.entry_dict_from_string(entry_string))

    return run_status_entries


def sql_tuples_to_delimited_strings(sql_tuples, delim="\t"):

    del_strings = list()

    for tup in sql_tuples:
        str_tup = [str(elem) for elem in tup]
        del_string = delim.join(str_tup)
        del_strings.append(del_string)

    return del_strings


def get_last_time_entry_string():

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM time_entries WHERE name_id = (SELECT MAX(name_id) FROM time_entries)')
    entry_string = sql_tuples_to_delimited_strings(c.fetchall(), delim='\t')
    conn.close()
    return entry_string[0]


def delete_last_time_entry():

    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM time_entries WHERE name_id = (SELECT MAX(name_id) FROM time_entries)')
    conn.commit()
    conn.close()


def check_successful_test_today():

    today_stamp = date_utils.get_current_date_string()

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM type_entries WHERE date_stamp="{date_stamp}" AND type_stamp="EVAL" AND completed=1'
              .format(date_stamp=today_stamp))
    tups = list()
    for tup in c:
        tups.append(tup)
    conn.close()
    return len(tups) > 0


def get_eval_runs():

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM type_entries WHERE type_stamp="TEST_EVAL" AND completed=1')
    entries = list()
    for entry in c:
        entry_string = '\t'.join([str(field) for field in entry])
        entries.append(RunStatus.entry_dict_from_string(entry_string))
    conn.close()
    return entries
