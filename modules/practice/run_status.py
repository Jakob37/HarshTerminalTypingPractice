import time


class RunStatus:

    def __init__(self, book, time_limit=None, error_limit=None, descr=None, is_eval_run=False):

        self.book = book

        self.start_time = time.time()
        self.errors = 0
        self.last_wrong = 0
        self.correct = 0
        self.prev_correct = 0

        self.wrong = 0
        self.current_target = self.book.current_line()
        self.current_written = ''
        self.is_game_over = False
        self.is_aborted = False
        self.return_struck = False
        self.description = descr
        self.is_eval_run = is_eval_run

        self.time_limit = time_limit
        self.error_limit = error_limit

    @staticmethod
    def entry_dict_from_string(entry_string, delim='\t'):

        entry_dict = dict()
        fields = entry_string.split(delim)
        entry_dict['entry_id'] = fields[0]
        entry_dict['date_stamp'] = fields[1]
        entry_dict['time_stamp'] = fields[2]
        entry_dict['typed_characters'] = int(fields[3])
        entry_dict['wpm'] = float(fields[4])
        entry_dict['completed'] = fields[5]
        entry_dict['total_time_seconds'] = float(fields[6])
        entry_dict['total_typed_characters'] = int(fields[7])
        entry_dict['total_errors'] = int(fields[8])
        entry_dict['type_stamp'] = fields[9]
        entry_dict['description'] = fields[10]
        return entry_dict

    def get_total_correct(self):
        return self.correct + self.prev_correct

    def is_completed(self, as_digit=False):
        is_completed_bool = self.errors < self.error_limit \
                                and self.get_elapsed_time() > self.time_limit
        if not as_digit:
            return is_completed_bool
        else:
            if is_completed_bool:
                return 1
            else:
                return 0

    def limited_run(self):
        return self.time_limit is not None or self.error_limit is not None

    def is_sentence_complete(self):
        return self.current_written == self.current_target

    def get_elapsed_time(self):
        return time.time() - self.start_time

    def new_loop(self):
        self.return_struck = False

    def check_limits(self):

        if self.time_limit is not None:
            if self.get_elapsed_time() > self.time_limit:
                self.is_game_over = True

        if self.error_limit is not None:
            if self.errors >= self.error_limit:
                self.is_game_over = True

    def new_line(self):
        self.current_target = self.book.get_next_line()
        self.last_wrong = 0
        self.prev_correct += self.correct
        self.correct = 0
        self.wrong = 0
        self.current_written = ''

    def check_char(self, new_char):

        if ord(new_char) == 127:   # Backspace
            self.current_written = self.current_written[:-1]
        elif ord(new_char) == 27:  # Escape
            print('\nQuitting...')
            self.is_game_over = True
            self.is_aborted = True
        elif len(self.current_written) < len(self.current_target):
            self.current_written += new_char
        elif ord(new_char) in (13, 32):
            self.return_struck = True

    def update_sentence_numbers(self):

        correct = 0
        wrong = 0

        target_sent = self.current_target
        actual_sent = self.current_written

        wrong_found = False
        for i in range(len(target_sent)):
            if i < len(actual_sent):

                target_letter = target_sent[i]
                actual_letter = actual_sent[i]

                if target_letter == actual_letter and not wrong_found:
                    correct += 1
                else:
                    wrong += 1
                    wrong_found = True

        self.correct = correct
        self.wrong = wrong

        if self.wrong > self.last_wrong:
            self.errors += 1
        self.last_wrong = self.wrong

    def get_wpm(self):

        prev_lines_chars = self.book.read_characters
        curr_line_chars = self.correct

        tot_chars = prev_lines_chars + curr_line_chars

        chars_per_word = 5
        wpm = (tot_chars / chars_per_word) / (self.get_elapsed_time() / 60)
        return wpm

    def __str__(self):

        return '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(self.get_total_correct(),
                                                   self.wrong,
                                                   self.start_time,
                                                   self.time_limit,
                                                   self.errors,
                                                   self.error_limit,
                                                   self.is_game_over)
