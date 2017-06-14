from modules.practice.book import Book


class BookRead:

    """
    Represents read-through of book
    """

    def __init__(self, book, line=0, spent_time=0, typos=list()):

        self.book = book
        self.line = line
        self.spent_time = spent_time
        self.typos = typos

    def update(self):
        pass

    def add_typo(self, typo):
        self.typos.append(typo)

    def load_from_db(self):
        pass

    def write_to_db(self):
        pass


class Typo:

    def __init__(self, character, curr_wpm, curr_epm):
        self.character = character
        self.curr_wpm = curr_wpm
        self.curr_epm = curr_epm

