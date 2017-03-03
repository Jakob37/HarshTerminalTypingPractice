import sqlite3

import harty_config

ENTRY_TABLE = 'type_entres'

ENTRY_FIELDS = [('entry_id', 'INTEGER PRIMARY KEY'),
                ('date_stamp', 'TEXT'),
                ('time_stamp', 'TEXT'),
                ('total_time_seconds', 'INTEGER'),
                ('total_typed_characters', 'INTEGER'),
                ('total_errors', 'INTEGER'),
                ('type_stamp', 'TEXT')]


def setup_database(database_path, dry_run=False):

    print('Attempting to open database at: {}'.format(database_path))

    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    create_entry_table = get_create_table_command(ENTRY_TABLE, ENTRY_FIELDS)
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


def insert_time_entry_into_database(time_entry, verbose=False):

    conn = get_connection()
    cursor = conn.cursor()

# ENTRY_FIELDS = [('entry_id', 'INTEGER PRIMARY KEY'),
#                 ('date_stamp', 'TEXT'),
#                 ('time_stamp', 'TEXT'),
#                 ('total_time_seconds', 'INTEGER'),
#                 ('total_typed_characters', 'INTEGER'),
#                 ('total_errors', 'INTEGER'),
#                 ('type_stamp', 'TEXT')]

    params = (time_entry.date,
              time_entry.time,
              time_entry.log_type,
              time_entry.focus,
              time_entry.duration,
              time_entry.message,
              time_entry.project,
              time_entry.work_type,)
    command_str = 'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?)'.format(table_name=ENTRY_TABLE)

    if verbose:
        print("Command to be executed: '{}'".format(command_str))

    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def list_entries_in_table(cursor, table_name):

    for row in cursor.execute('SELECT * FROM {}'.format(table_name)):
        string_values = [str(val) for val in row]
        print('\t'.join(string_values))


def get_time_entries_as_strings(sep="\t"):

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM time_entries')
    time_entry_strings = sql_tuples_to_delimited_strings(c.fetchall(), delim=sep)
    conn.close()
    return time_entry_strings


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
