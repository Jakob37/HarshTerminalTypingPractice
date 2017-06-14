from modules.practice.book import Book
from modules.database import book_db_interface


class BookRead:

    """
    Represents read-through of book
    """

    def __init__(self, book, name, line=0, spent_time=0, typos=list()):

        self.book = book
        self.name = name
        self.line = line
        self.spent_time = spent_time
        self.typos = typos

    def update(self):
        pass

    def add_typo(self, typo):
        self.typos.append(typo)

    def load_from_db(self):
        pass

    def write_new_db_entry(self):
        book_db_interface.add_new_book(self.name, self.book.book_fp)


class Typo:

    def __init__(self, character, curr_wpm, curr_epm):
        self.character = character
        self.curr_wpm = curr_wpm
        self.curr_epm = curr_epm
