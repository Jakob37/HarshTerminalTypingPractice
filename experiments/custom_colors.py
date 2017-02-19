#!/usr/bin/env python3

# Using environment colors
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python



from termcolor import colored
print(colored('hello', 'red'), colored('world', 'green'))


# Colorama seems nice for cross-platform coloring
# https://pypi.python.org/pypi/colorama

from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')


