import pygame
from random import randint

pygame.init()
win = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Map Generator')
clock = pygame.time.Clock()
colourmap = {0: (85, 145, 10), 1: (90, 90, 90), 2: (28, 41, 122)}
bordermap = {0: (65, 125, 0), 1: (70, 70, 70), 2: (8, 21, 102)}


# /////////////////////////////////////////////////////// ----- //////////////////////////////////////////////////////
def create_border_river(boardmap):
    flag1 = randint(0, 1)
    flag2 = randint(0, 1)
    print(flag1, flag2)
    if flag1:
        start = [flag2 * 19, randint(0, 19)]
    else:
        start = [randint(0, 19), flag2 * 19]

    boardmap[start[0]][start[1]] = 2

    # direction = some coordinate
    # then get diection to coord using subtraction and sign(result)
    # use direction (with weighted values) to step (recursion?) create more river tiles.
    return boardmap
# /////////////////////////////////////////////////////// ----- //////////////////////////////////////////////////////


board = []
for a in range(20):
    row = []
    for b in range(20):
        row.append(randint(0,1))
    board.append(row)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            board = create_border_river(board)

    win.fill((0, 0, 0))
    for y, row in enumerate(board):
        for x, square in enumerate(row):
            pygame.draw.rect(win, bordermap[square], (x * 40, y * 40, 40, 40))
            pygame.draw.rect(win, colourmap[square], (x * 40 + 2, y * 40 + 2, 36, 36))

    pygame.display.flip()
