harty_log = 'harty.log'

def write_to_log(text):

	with open(harty_log, 'a') as out_fh:
		print(text, file=out_fh)
