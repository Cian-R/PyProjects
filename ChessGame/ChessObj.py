import math
import pygame
from random import randint


def rounddown(x):
    return int(math.floor(x / 75.0)) * 75


def DrawBoard():
    pygame.draw.rect(win, (255, 255, 255), (10, 10, 600, 600))
    for y in range(8):
        if y % 2 != 0:
            mod = 0
        else:
            mod = 75
        for x in range(4):
            pygame.draw.rect(win, (40, 40, 40), (10 + mod + (x * 150), 10 + (y * 75), 75, 75))


pygame.init()
bg_colour = (100, 100, 100)

pygame.font.init()
titlefont = pygame.font.SysFont('lucidaconsole', 70)
selecfont = pygame.font.SysFont('lucidaconsole', 20)
bfont = pygame.font.SysFont('lucidaconsole', 40)

win = pygame.display.set_mode((620, 620))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()

sprite_sheet = pygame.image.load('Sprites/sprite_sheet.png').convert_alpha()
sprite_sheet = pygame.transform.scale(sprite_sheet, (480, 160))


# /////////////////////////////////////////////////// Setup Classes //////////////////////////////////////////////////

class Square:

    def __init__(self, colour, piece, coords):
        if colour:
            self.colour = whiteSq
        else:
            self.colour = blackSq
        self.piece = piece
        self.coords = coords
        self.truepos = [10 + (coords[0] * 75), 10 + (coords[1] * 75)]

    def __str__(self):
        return str(self.colour) + str(self.piece) + str(self.coords)

    def __repr__(self):
        return str(self.colour) + str(self.piece) + str(self.coords)

    def draw(self):
        mousepos = pygame.mouse.get_pos()
        if (self.truepos[0] < mousepos[0] < (self.truepos[0] + 75)) and \
                (self.truepos[1] < mousepos[1] < (self.truepos[1] + 75)):
            pygame.draw.rect(win, (50, 200, 50), (self.truepos[0], self.truepos[1], 75, 75))
        else:
            pygame.draw.rect(win, self.colour, (self.truepos[0], self.truepos[1], 75, 75))

        if self.piece != 0:
            pygame.draw.rect(win,
                             (100, 100, 100),
                             (self.truepos[0], self.truepos[1], 55, 55))

    def setPiece(self, value):
        self.piece = value


class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        # sprite.set_colorkey(())
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////// Setup //////////////////////////////////////////////////////
whiteSq = (238, 238, 210)
blackSq = (118, 150, 86)

board = []
flag = True

# Initiate squares
for board_x in range(8):
    row = []
    for board_y in range(8):
        row.append(Square(flag, 0, [board_x, board_y]))
        flag = not flag

    print(row)
    board.append(row)
    flag = not flag

board[7][0].setPiece(7)
board[3][1].setPiece(2)

print("")
for row in board:
    print(row)
# main_spritesheet = Spritesheet(None)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////// Main ///////////////////////////////////////////////////////

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # ==================== GRAPHICS DRAWING ====================
    win.fill(bg_colour)

    # DrawBoard()
    # for square in squares:
    #     square.draw()
    for row in board:
        for square in row:
            square.draw()
    # =========================================================
    win.blit(sprite_sheet, (100, 400))
    pygame.display.update()
    clock.tick(20)
