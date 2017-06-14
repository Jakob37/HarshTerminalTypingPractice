import random


class Book:
    def __init__(self, book_fp, start_line=1, rand_start=False):

        self.book_lines = Book.load_book(book_fp)
        self.book_fp = book_fp

        if not rand_start:
            self.curr_line_nbr = start_line
        else:
            self.curr_line_nbr = random.randint(0, len(self.book_lines))

        self.read_lines = 0
        self.read_words = 0
        self.read_characters = 0

    def get_line_number(self):
        return self.curr_line_nbr

    def get_book_name(self):
        # return self.book_fp.split()
        return self.book_fp.split('/')[-1].split('.')[0].replace('_', ' ').capitalize()

    @staticmethod
    def load_book(book_fp):

        book_lines = list()

        with open(book_fp) as book_fh:
            for line in book_fh:
                line = line.strip()
                if line != '':
                    book_lines.append(line)
        return book_lines

    def get_preceeding_lines(self, nbr):
        curr = self.curr_line_nbr
        return self.book_lines[curr - nbr - 1:curr - 1]

    def get_following_lines(self, nbr):
        curr = self.curr_line_nbr
        return self.book_lines[curr:curr + nbr]

    def current_line(self):

        print(self.curr_line_nbr)

        return self.book_lines[self.curr_line_nbr - 1]

    def get_next_line(self, update_line=True):

        previous_line = self.book_lines[self.curr_line_nbr - 1]
        if update_line:
            self.curr_line_nbr += 1
            self.read_lines += 1
            self.read_words += len(previous_line.split(' '))
            self.read_characters += len(previous_line)
        # self.wpm_updated = False
        curr_line = self.book_lines[self.curr_line_nbr - 1]
        return curr_line
