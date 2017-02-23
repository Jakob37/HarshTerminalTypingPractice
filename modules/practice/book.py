
class Book:

	def __init__(self, book_fp, start_line=1):

		self.book_fh = open(book_fp)
		for skipped in range(start_line):
			next(self.book_fh)

	def get_next_line(self):

		next_line = ''
		while next_line == '':
			next_line = next(self.book_fh)
			next_line = next_line.rstrip()

		return next_line

	def close_book(self):
		self.book_fh.close()
