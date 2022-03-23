from random import randint
import pygame
import math


def rounddown(x):
    return int(math.floor(x / 75.0)) * 75


def DrawBoard(pieces):
    pygame.draw.rect(win, (255, 255, 255), (10, 10, 600, 600))
    for y in range(8):
        if y % 2 != 0:
            mod = 0
        else:
            mod = 75
        for x in range(4):
            pygame.draw.rect(win, (40, 40, 40), (10 + mod + (x*150), 10 + (y*75), 75, 75))

    # for obj in pieces:
    pygame.draw.circle(win, (200, 200, 200), (45, 45), 35)

    mousepos = pygame.mouse.get_pos()

    pygame.draw.rect(win, (50, 150, 50), (10 + (rounddown(mousepos[0]-10)), 10 + (rounddown(mousepos[1]-10)), 75, 75))

    return None


pygame.init()
bg_colour = (100, 100, 100)

pygame.font.init()
titlefont = pygame.font.SysFont('lucidaconsole', 70)
selecfont = pygame.font.SysFont('lucidaconsole', 20)
bfont = pygame.font.SysFont('lucidaconsole', 40)

win = pygame.display.set_mode((620, 620))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////// Setup Screen ///////////////////////////////////////////////////
pieces = {'wp1': [0, 1], 'wp2': [1, 1], 'wp3': [2, 1], 'wp4': [3, 1], 'wp5': [4, 1], 'wp6': [5, 1], 'wp7': [6, 1],
          'wp8': [7, 1]}
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # ==================== GRAPHICS DRAWING ====================
    win.fill(bg_colour)
    DrawBoard(pieces)
    # =========================================================
    pygame.display.update()
    clock.tick(20)
