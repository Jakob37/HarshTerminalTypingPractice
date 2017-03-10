
from modules.database import database_interface


def main(args):

    if args.highscore:
        show_highscore(args)
    else:
        show_day_tests(args)


def show_highscore(args):

    today_runs = database_interface.get_today_test_eval_runs()
    best_run = today_runs[0]
    for run in today_runs[1:]:

        wpm = run[4]
        errors = run[8]

        if errors < best_run[8]:
            best_run = run
        elif errors == best_run[8]:
            if wpm < best_run[4]:
                best_run = run

    print('Best for today: {:.2f} wpm, {} errors'.format(best_run[4], best_run[8]))


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
