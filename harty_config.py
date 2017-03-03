import os
import configparser
import sys

from modules.database import database_interface

expected_conf_fields = [('file_paths', 'sql_path')]

CONF_NAME = 'harty.conf'

my_dir = os.path.dirname(os.path.realpath(__file__))
conf_path = "{}/{}".format(my_dir, CONF_NAME)

config = None
config_exists = os.path.isfile(conf_path)

if config_exists:
    config = configparser.ConfigParser()
    config.read(conf_path)


def check_config_exists():
    return config_exists


def generate_default_config():

    setup_config_file()
    setup_database()


def check_database_exists():

    if not check_config_exists():
        print("Config file not found, not able to check database")
        sys.exit(1)

    db_path = config.get('file_paths', 'sql_path')
    db_exists = os.path.isfile(db_path)

    if db_exists:
        return True
    else:
        print('Database not found at specified path: {}'.format(db_path))
        print('Please setup this properly by running the \'harty setup\' command')
        sys.exit(1)


def get_expected_field_not_present():

    expected_fields_not_present = list()

    for field in expected_conf_fields:

        category, value = field
        has_option = config.has_option(category, value)

        if not has_option:
            expected_fields_not_present.append((category, value))

    return expected_fields_not_present


def get_config_path():

    return conf_path


def get_config(force_reload=False):

    if force_reload:
        conf_exist = os.path.isfile(conf_path)

        if conf_exist:
            conf = configparser.ConfigParser()
            conf.read(conf_path)
            return conf

    if not config_exists:
        raise Exception("Config file not found at expected path: {}, run setup command (harty.py setup) to get started"
                        .format(conf_path))

    return config


def setup_config_file():

    initial_basedir = my_dir
    new_config = configparser.RawConfigParser()

    new_config.add_section('file_paths')
    new_config.set('file_paths', 'sql_path', '%(output_base)s/harty_data.sqlite')
    new_config.set('file_paths', 'book_base', '%(output_base)s/books')
    new_config.set('file_paths', 'output_base', initial_basedir)

    new_config.add_section('settings')
    new_config.set('settings', 'error_threshold', 15)
    new_config.set('settings', 'time_threshold', 60)
    new_config.set('settings', 'typer', 'default')

    # conf_path = '{}/{}'.format(initial_basedir, 'harty.conf')

    print("Writing config file to {}".format(conf_path))

    with open(conf_path, 'w') as config_fh:
        new_config.write(config_fh)
        print('Config written!')


def setup_database():

    """Setup SQLite database with tables used by harty at path specified by config file"""

    print("Setting up database...")
    # conf = harty_config.get_config(force_reload=True)

    local_conf = get_config(force_reload=True)

    database_path = local_conf.get('file_paths', 'sql_path')
    database_interface.setup_database(database_path)
    print("Database written to {}".format(database_path))