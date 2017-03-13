
from modules.database import database_interface
from modules.utils import date_utils


def main(args):

    if args.highscore:
        show_highscore(args)
    else:
        show_day_tests(args)


def show_highscore(args):

    runs = database_interface.get_eval_runs()

    if args.highscore == 'day':
        today_stamp = date_utils.get_current_date_string()
        date_range_runs = [e for e in runs if e['date_stamp'] == today_stamp]
    elif args.highscore == 'week':
        week_start_stamp = date_utils.get_start_of_week()
        date_range_runs = [e for e in runs if e['date_stamp'] >= week_start_stamp]
    elif args.highscore == 'month':
        month_start_stamp = date_utils.get_start_of_month()
        date_range_runs = [e for e in runs if e['date_stamp'] >= month_start_stamp]
    elif args.highscore == 'year':
        year_start_stamp = date_utils.get_start_of_year()
        date_range_runs = [e for e in runs if int(e['date_stamp']) >= int(year_start_stamp)]
    else:
        raise ValueError('Unknown option: {}'.format(args.highscore))

    if len(date_range_runs) > 0:

        best_run = date_range_runs[0]
        for run in date_range_runs[1:]:

            wpm = run['wpm']
            errors = run['total_errors']

            if errors < best_run['total_errors']:
                best_run = run
            elif errors == best_run['total_errors']:
                if wpm > best_run['wpm']:
                    best_run = run
        print('Best for {}:\t{:.2f} wpm\t{} errors\t{}'
              .format(args.highscore, best_run['wpm'], best_run['total_errors'], best_run['date_stamp'])
              .expandtabs(tabsize=6))
    else:
        print('Best for {}:\t{:.2f} wpm\t{} errors\t{}'.format(args.highscore, 0, 100, date_utils.get_current_date_string()))


def show_day_tests(args):

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
