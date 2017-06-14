from modules.practice.book import Book
from modules.book.book_read import BookRead

from modules.practice import practice_with_display

def read_book(args):

    print('main called')
    book_path = args.book
    book = Book(book_path)
    practice_with_display.run_practice_with_display(book, book_read)


def add_book(args):

    book_path = args.path
    book = Book(book_path)

    book_name = args.name
    book_read = BookRead(book, book_name)
    book_read.write_new_db_entry()

    print('New book "{}" with path "{}" saved'.format(book_name, book_path))

