import time #to use for measuring methods exec time

def array_print(array):
    for row in array:
        for cell in row:
            print(cell, end=" ")
        print()

def init_board(n):
    array = [[0] * n for i in range(n)]
    #todo color regions
    return array

n = 10
k = 2
board = init_board(n)
array_print(board)