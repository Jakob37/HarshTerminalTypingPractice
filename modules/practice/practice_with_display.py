import curses
import sys

from modules.utils.getch import _Getch
from modules.practice import practice_visualize_funcs as vis

from modules.practice.run_status import RunStatus
from modules.database import database_interface

from modules.practice import output_messages

g = _Getch()


MIN_HEIGHT = 20


def run_practice_with_display(book, auto_return=True, time_limit=None, error_limit=None,
                              descr="", is_eval_run=False, book_read=None):

    starting_line_nbr = book.get_line_number()

    STATUS_STRING = 'How much can you time in {} seconds? But don\'t get sloppy - {} errors and you are done!\n' \
                    '\t  Reading from the book "{}", starting at line: {}'.format(time_limit,
                                                                            error_limit,
                                                                            book.get_book_name(),
                                                                            starting_line_nbr)
    window = initialize_curses_window()
    run_status = RunStatus(book, time_limit=time_limit, error_limit=error_limit, descr=descr, is_eval_run=is_eval_run)

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
                run_status.check_limits()

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

        output_messages.practice_message(run_status)

        if not run_status.is_aborted and book_read is not None:
            database_interface.write_run_entry(run_status)


def initialize_curses_window():

    window = curses.initscr()
    curses.start_color()
    curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    return window
