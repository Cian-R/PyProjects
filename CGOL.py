import pygame
import random


pygame.init()
BOARD_HEIGHT = 60
BOARD_WIDTH = 80
win = pygame.display.set_mode((BOARD_WIDTH*10, BOARD_HEIGHT*10))
pygame.display.set_caption('CGOL')
clock = pygame.time.Clock()


# generate board state
# [[0 for _ in range(y)] for _ in range(x)]
set_squares = [[31, 1], [33, 1], [32, 2], [33, 2], [32, 3],
               [22, 21], [23, 22], [21, 23], [22, 23], [23, 23]]


def pick_value(y, x):
    # if random.randint(0, 100) > 80:
    #     return 1
    # else:
    #     return 0
    if (x + y > 75) and (x + y < 80): return random.randint(0, 1)
    if [x, y] in set_squares:
        return 1
    else:
        return 0


board_state = [[pick_value(y, x) for x in range(80)] for y in range(60)]
# print(str(line) for line in board_state)


def get_neighbours_count(board, y, x):
    directions = [-1, 0, 1]
    neighbours = 0
    for ymod in directions:
        ynew = y + ymod
        if ynew > BOARD_HEIGHT - 1: ynew = 0
        elif ynew < 0: ynew = BOARD_HEIGHT - 1

        for xmod in directions:
            xnew = x + xmod
            if xnew > BOARD_WIDTH - 1: xnew = 0
            elif xnew < 0: xnew = BOARD_WIDTH - 1

            if ymod == xmod == 0:
                # print(xnew, ynew, "is the middle")
                pass
            elif board[ynew][xnew] == 1:
                # print(xnew, ynew, "is a neighbouring 1")
                neighbours += 1
            else:
                # print(xnew, ynew, "--")
                pass
    return neighbours


def update_board(board):
    copy_board = [row[:] for row in board]
    for yval in range(len(board)):
        for xval in range(len(board[yval])):
            neighbours = get_neighbours_count(board, yval, xval)
            if neighbours < 2:
                copy_board[yval][xval] = 0  # Die - Underpopulation
            elif (neighbours == 3) and (board[yval][xval] == 0):
                copy_board[yval][xval] = 1  # Born - Reproduction
            elif neighbours < 4:
                copy_board[yval][xval] = board[yval][xval]  # Live
            else:
                copy_board[yval][xval] = 0  # Die - Overpopulation
    board = [row[:] for row in copy_board]
    return board



def draw_board(board):
    for yval in range(len(board)):
        for xval in range(len(board[yval])):
            # r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            r, g, b = (0, 0, 0) if board[yval][xval] == 0 else (255, 255, 255)
            pygame.draw.rect(win, (r, g, b, 50), (0 + (xval * 10), 0 + (yval * 10), 10, 10))

    # border_colour = pygame.Color(255, 255, 255, a=1)
    # for yval in range(int(BOARD_HEIGHT)):
    #     pygame.draw.rect(win, border_colour, (0, 0+(yval*10), BOARD_WIDTH*10, 1))
    # for xval in range(int(BOARD_WIDTH)):
    #     pygame.draw.rect(win, border_colour, (0+(xval*10), 0, 1, BOARD_HEIGHT*10))


# for gra in board_state:
#     print(gra)
active = False

while True:
    win.fill((0, 0, 0))
    if active:
        board_state = update_board(board_state)
    draw_board(board_state)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                active = True
            if event.key == pygame.K_s:
                x, y = pygame.mouse.get_pos()
                pygame.draw.rect(win, (100, 255, 100), ((x // 10) * 10, (y // 10) * 10, 10, 10))
                print("\nChecking out", x // 10, y // 10)
                print(get_neighbours_count(board_state, y // 10, x // 10))
    pygame.display.update()
    clock.tick(20)
