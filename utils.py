WHITE = '\033[7m'
BLACK = '\033[40m'
RED = '\033[41m'
GREEN = '\033[42m'
YELLOW = '\033[43m'
BLUE = '\033[44m'
PURPLE = '\033[45m'
CYAN = '\033[46m'
GREY = '\033[100m'
ALT_RED = '\033[101m'
ALT_BLUE = '\033[104m'
RESET = '\033[0m'
BOLD = '\033[1m'
COLORS = [WHITE,BLACK,RED,GREEN,YELLOW,BLUE,PURPLE,CYAN,GREY,ALT_RED,ALT_BLUE]

def print_grid(array):
    for row in array:
        for cell in row:
            print(cell, end=" ")
        print()
    print()