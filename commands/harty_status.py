from modules.database import database_interface


def main(args):

    eval_run_today = database_interface.check_successful_test_today()

    if not args.terminal:
        if eval_run_today:
            print('Run done today')
        else:
            print('Run NOT done today')
    else:
        if not eval_run_today:
            print('Run "harty test" today!')
