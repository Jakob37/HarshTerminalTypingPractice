
class Book:

	def __init__(self, book_fp, start_line=0, preview_size=3):

		# self.preceeding_lines = list()
		# self.current_line = None
		# self.coming_lines = list()

		self.book_lines = self.load_book(book_fp)
		self.curr_line_nbr = start_line
		self.read_lines = 0

		# self.book_fh = open(book_fp)
		# for skipped in range(start_line):
		# 	skipped = next(self.book_fh)
		# 	self.preceeding_lines.append(skipped)

	def load_book(self, book_fp):

		book_lines = list()

		with open(book_fp) as book_fh:
			for line in book_fh:
				line = line.strip()
				if line != '':
					book_lines.append(line)
		return book_lines


	def get_preceeding_lines(self, nbr):
		curr = self.curr_line_nbr
		return self.book_lines[curr-nbr-1:curr-1]


	def get_following_lines(self, nbr):
		curr = self.curr_line_nbr
		return self.book_lines[curr+1:curr+1+nbr]


	def current_line(self):
		return self.book_lines[self.curr_line_nbr - 1]


	def get_next_line(self, update_line=True):

		if update_line:
			self.curr_line_nbr += 1
			self.read_lines += 1
		curr_line = self.book_lines[self.curr_line_nbr - 1]
		return curr_line


	# def get_next_line(self):

	# 	next_line = ''
	# 	while next_line == '':
	# 		next_line = next(self.book_fh)
	# 		next_line = next_line.rstrip()

	# 	return next_line

	# def close_book(self):
	# 	self.book_fh.close()
