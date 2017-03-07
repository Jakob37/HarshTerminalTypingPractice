
from modules.database import database_interface


def main(args):

    tabsize = 10

    print('Date\twpm\terrors'.expandtabs(tabsize=tabsize))

    entry_dicts = database_interface.get_run_entry_dicts()
    for entry_dict in entry_dicts:
        if entry_dict['type_stamp'] == 'EVAL' and entry_dict['completed'] == '1':
            print('{date}\t{wpm:.2f}\t{errors}'.format(
                date=entry_dict['date_stamp'],
                wpm=entry_dict['wpm'],
                errors=entry_dict['total_errors']
            ).expandtabs(tabsize=tabsize))





