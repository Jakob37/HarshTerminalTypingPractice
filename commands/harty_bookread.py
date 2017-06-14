from modules.practice.book import Book
from modules.book.book_read import BookRead


def read_book(args):

    print('main called')


def add_book(args):

    book_path = args.book
    book = Book(book_path)

    book_read = BookRead(book)

    # print(book.book_lines)

    print('add new book called')


