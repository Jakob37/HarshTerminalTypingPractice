import curses
import sys

from modules.utils.getch import _Getch
from modules.practice import practice_visualize_funcs as vis

from modules.practice.run_status import RunStatus
from modules.database import database_interface

g = _Getch()


MIN_HEIGHT = 20


def run_practice_with_display(book, auto_return=False, time_limit=None, error_limit=None, descr=""):

    starting_line_nbr = book.get_line_number()

    STATUS_STRING = 'How much can you time in {} seconds? But don\'t get sloppy - {} errors and you are done!\n' \
                    '\t  Reading from the book "{}", starting at line: {}'.format(time_limit,
                                                                            error_limit,
                                                                            book.get_book_name(),
                                                                            starting_line_nbr)

    # log_util.write_to_log('New run started')

    window = initialize_curses_window()
    run_status = RunStatus(book, time_limit=time_limit, error_limit=error_limit, descr=descr)

    try:
        (h, w) = window.getmaxyx()
        write_center = int(h/2)

        if h < MIN_HEIGHT:
            print('Your terminal is too small! Make it taller and try again')
            sys.exit(1)

        x_margin = 10

        vis.visualize(window, write_center, x_margin, run_status, debug_string=STATUS_STRING)

        while not run_status.is_game_over:

            run_status.new_loop()

            new_char = g()
            run_status.check_char(new_char)
            run_status.update_sentence_numbers()

            if run_status.is_sentence_complete() and (run_status.return_struck or auto_return):
                run_status.new_line()

            vis.visualize(window, write_center, x_margin, run_status, debug_string=STATUS_STRING)

            if run_status.limited_run():
                # print('check limited')
                run_status.check_limits()

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

        if run_status.errors > run_status.get_total_correct():
            text_prefix = 'More errors than correct? Pull yourself together, ' \
                          'and make sure that CapsLock isn\'t enabled'
        elif run_status.errors == 0:
            text_prefix = 'Well done, no errors! Keep it up!'
        elif run_status.errors <= 3:
            text_prefix = 'Almost there, make it zero errors next time!'
        elif run_status.errors <= 5:
            text_prefix = 'You are getting sloppy, keep track of those fingers and get the errors down to zero!'
        elif run_status.errors <= 10:
            text_prefix = 'You need to be more careful while typing, place those fingers correctly!'
        elif run_status.errors <= 14:
            text_prefix = 'Not good, start thinking before typing!!'
        else:
            text_prefix = 'Terrible! So many errors, are you even trying?'

        if not run_status.is_aborted:
            print('\n{}\nIt took {:.1f} seconds, you made {} errors, {} correct, wpm: {:.2f}'
                  .format(text_prefix, run_status.get_elapsed_time(), run_status.errors,
                          run_status.get_total_correct(), run_status.get_wpm()))
            database_interface.write_run_entry(run_status)
            print('Entry written to database')
        else:
            print('User aborted after {:.1f} seconds, errors: {} wpm {:.2f}'.format(run_status.get_elapsed_time(),
                                                                                    run_status.errors,
                                                                                    run_status.get_wpm()))


def initialize_curses_window():

    window = curses.initscr()
    curses.start_color()
    curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    return window


