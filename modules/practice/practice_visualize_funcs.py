import time
import curses

def visualize(window, write_center, x_margin, sentence, correct, wrong, errors, start_time):

    window.clear()
    status_sentence = get_status_string(start_time, correct, errors)

    window.addstr(write_center - 2, x_margin, "statusstr", curses.color_pair(curses.COLOR_GREEN))
    window.addstr(write_center + 2, x_margin, status_sentence)
    write_colored_sentence(window, x_margin, write_center + 3, sentence, correct, wrong)

    window.refresh()


def write_colored_sentence(window, x, y, target_sent, correct, wrong):

    corr_str = target_sent[:correct]
    wrong_str = target_sent[correct:correct+wrong]
    rest = target_sent[correct+wrong:]

    window.addstr(y, x, corr_str, curses.color_pair(curses.COLOR_GREEN))
    window.addstr(y, x + len(corr_str), wrong_str, curses.color_pair(curses.COLOR_RED))
    window.addstr(y, x + len(corr_str) + len(wrong_str), rest)
    window.move(y, x + len(corr_str) + len(wrong_str))


def get_status_string(start_time, correct, wrong):

    elapsed_time = time.time() - start_time
    return '{} seconds, {} correct, {} errors'.format(int(elapsed_time), correct, wrong)
