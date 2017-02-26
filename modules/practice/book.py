import random


class Book:

	def __init__(self, book_fp, start_line=1, preview_size=3, rand_start=False):

		# self.preceeding_lines = list()
		# self.current_line = None
		# self.coming_lines = list()

		self.book_lines = self.load_book(book_fp)

		if not rand_start:
			self.curr_line_nbr = start_line
		else:
			self.curr_line_nbr = random.randint(0, len(self.book_lines))

		self.read_lines = 0
		self.read_words = 0
		self.read_characters = 0

		self.wpm_updated = True
		self.wpm = 0

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
		return self.book_lines[curr:curr+nbr]


	def current_line(self):
		return self.book_lines[self.curr_line_nbr - 1]


	def get_next_line(self, update_line=True):

		previous_line = self.book_lines[self.curr_line_nbr - 1]
		if update_line:
			self.curr_line_nbr += 1
			self.read_lines += 1
			self.read_words += len(previous_line.split(' '))
			self.read_characters += len(previous_line)
			self.wpm_updated = False
		curr_line = self.book_lines[self.curr_line_nbr - 1]
		return curr_line


	def get_wpm(self, elapsed_time):

		if not self.wpm_updated:
			self.wpm_updated = True
			self.wpm = self.read_words / (elapsed_time / 60)

		return self.wpm

