# from modules.practice.book import Book
# from modules.database import book_db_interface


class BookRead:

    """
    Represents read-through of book
    """

    def __init__(self, name, path, line=0, spent_time=0, typos=list()):

        self.name = name
        self.path = path
        self.line = line
        self.spent_time = spent_time
        self.typos = typos

    @classmethod
    def book_read_from_string(cls, tab_string):

        """Generate object from tab-delimited string"""

        fields = tab_string.split('\t')
        name = fields[0]
        path = fields[1]
        progress = fields[2]
        spent_time = fields[3]

        new_obj = cls(name=name, path=path, line=progress, spent_time=spent_time)
        return new_obj

    def update(self):
        pass

    def add_typo(self, typo):
        self.typos.append(typo)

    def load_from_db(self):
        pass

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}'.format(self.name, self.path, self.line, self.spent_time, self.typos)


class Typo:

    def __init__(self, character, curr_wpm, curr_epm):
        self.character = character
        self.curr_wpm = curr_wpm
        self.curr_epm = curr_epm
