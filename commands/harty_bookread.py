from modules.practice.book import Book
from modules.book.book_read import BookRead

from modules.practice import practice_with_display
from modules.database import book_db_interface




def read_book(args):

    print('main called')
    book_name = args.name

    target_read = book_db_interface.load_book(book_name)

    print(target_read)


def add_book(args):

    book_path = args.path
    book = Book(book_path)

    book_name = args.name
    book_read = BookRead(book, book_name)

    book_db_interface.add_new_book(book_read.name, book_read.path)
