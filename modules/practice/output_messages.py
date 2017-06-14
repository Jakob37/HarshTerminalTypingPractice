def practice_message(run_status):
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
        print('Entry written to database')
    else:
        print('User aborted after {:.1f} seconds, errors: {} wpm {:.2f}'.format(run_status.get_elapsed_time(),
                                                                                run_status.errors,
                                                                                run_status.get_wpm()))
