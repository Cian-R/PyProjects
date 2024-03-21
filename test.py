import random

board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

print("Board:", board)
print("Copy:")

copy_board = [row[:] for row in board]
print("Copy post copy:", copy_board)

board[1][1] = 1
copy_board[2][2] = 1
print("Edits made===================================")
print("Board:", board)
print("Copy:", copy_board)
assert copy_board[1][1] == 0
assert board[2][2] == 0



for yval in range(len(board)):
    for xval in range(len(board[yval])):
        neighbours = random.randint(0, 7)
        if neighbours < 2:
            print(neighbours, "<2")
            copy_board[yval][xval] = 0  # Die - Underpopulation
        elif (neighbours == 3) and (board[yval][xval] == 0):
            print(neighbours, "born")
            copy_board[yval][xval] = 1  # Born - Reproduction
        elif neighbours < 4:
            print(neighbours, "<4")
            copy_board[yval][xval] = board[yval][xval]  # Live
        else:
            print(neighbours, "L")
            copy_board[yval][xval] = 0  # Die - Overpopulation

print(board)
print(copy_board)
print("==========v==========")
board = [row[:] for row in copy_board]

print(board)
print(copy_board)
