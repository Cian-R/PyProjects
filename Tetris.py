from random import randint
import pygame


def VarProxSearch(grid, x, y, searchrange, target):
    rangelis = [x for x in range(-searchrange, searchrange + 1)]
    sign = lambda integer_val: (integer_val > 0) - (integer_val < 0)
    count = 0
    for xmod in rangelis:
        for ymod in rangelis:
            try:
                xnew, ynew = (x + xmod), (y + ymod)
                if (sign(xnew) != -1) and (sign(ynew) != -1):
                    if grid[xnew][ynew] == target:
                        count += 1
            except:
                pass
    return count


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def button(screen, msg, x, y, w, h, ic, ac, action=None):
    bmouse = pygame.mouse.get_pos()
    bclick = pygame.mouse.get_pressed()
    if x + w > bmouse[0] > x and y + h > bmouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if (bclick[0] == 1) and (action is not None):
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


def valbutton(screen, msg, x, y, w, h, ic, ac, val):
    vmouse = pygame.mouse.get_pos()
    vclick = pygame.mouse.get_pressed()
    if x + w > vmouse[0] > x and y + h > vmouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if vclick[0] == 1:
            return val
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (int(x + (w / 2)), int(y + (h / 2)))
    screen.blit(textSurf, textRect)
    return 0


def triggerTest():
    for apiece in curr:
        if apiece[1] == 19:
            return True
        else:
            for block in board:
                if (apiece[0] == block[0]) and (apiece[1] == (block[1] - 1)):
                    return True
    return False


def drawAll():
    for obj in curr:
        pygame.draw.rect(win, obj[2], (obj[0] * 30, obj[1] * 30, 30, 30))
        pygame.draw.rect(win, obj[3], (obj[0] * 30 + 3, obj[1] * 30 + 3, 24, 24))

    for obj in board:
        pygame.draw.rect(win, obj[2], (obj[0] * 30, obj[1] * 30, 30, 30))
        pygame.draw.rect(win, obj[3], (obj[0] * 30 + 3, obj[1] * 30 + 3, 24, 24))


def pickPiece():
    return pieceSelection[randint(0, len(pieceSelection)-1)]


pygame.init()
bg_colour = (30, 0, 0)

pygame.font.init()
titlefont = pygame.font.SysFont('lucidaconsole', 70)
selecfont = pygame.font.SysFont('lucidaconsole', 20)
bfont = pygame.font.SysFont('lucidaconsole', 40)

win = pygame.display.set_mode((300, 600))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()

ghostSurf = pygame.Surface((300, 600))  # the size of your rect
ghostSurf.set_alpha(100)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////// Setup Screen ///////////////////////////////////////////////////
timer = 0
board = []
curr = [
    [3, 0, (50, 150, 150), (30, 130, 130)],
    [3, 1, (50, 150, 150), (30, 130, 130)],
    [3, 2, (50, 150, 150), (30, 130, 130)]
]

pieceSelection = [
    [
        [3, 0, (50, 150, 150), (30, 130, 130)],
        [3, 1, (50, 150, 150), (30, 130, 130)],
        [3, 2, (50, 150, 150), (30, 130, 130)]
    ], [
        [3, 0, (150, 50, 150), (130, 30, 130)],
        [3, 1, (150, 50, 150), (130, 30, 130)],
        [4, 1, (150, 50, 150), (130, 30, 130)]
    ], [
        [3, 0, (150, 150, 50), (130, 130, 30)],
        [3, 1, (150, 150, 50), (130, 130, 30)],
        [2, 1, (150, 150, 50), (130, 130, 30)],
        [4, 1, (150, 150, 50), (130, 130, 30)]
    ], [
        [3, 0, (150, 150, 150), (130, 130, 130)],
        [3, 1, (150, 150, 150), (130, 130, 130)],
        [4, 0, (150, 150, 150), (130, 130, 130)],
        [4, 1, (150, 150, 150), (130, 130, 130)]
    ]
]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for brick in curr:
                    if brick[0] != 0: brick[0] -= 1
            if event.key == pygame.K_RIGHT:
                for brick in curr:
                    if brick[0] != 9: brick[0] += 1
            if event.key == pygame.K_DOWN:
                while not triggerTest():
                    for brick in curr:
                        brick[1] += 1

    if triggerTest():
        for brick in curr:
            board.append(list(brick))
        curr = pickPiece()

    timer += 1
    # if timer == 7:
    #     for p in board:
    #         print(p)
    #     print("===================")
    if timer == 15:
        for p in board:
            print(p)
        print("===================")
        timer = 0
        for brick in curr:
            brick[1] += 1


    # ==================== GRAPHICS DRAWING ====================
    win.fill(bg_colour)
    ghostSurf.fill(bg_colour)

    # Draw Ghost
    difference = 21
    ghost = []
    for nothing in curr:
        ghost.append(nothing)
    for brick in ghost:
        dist = 19 - brick[1]
        if dist < difference: difference = dist
        for piece in board:
            if brick[0] == piece[0]:
                dist = piece[1] - brick[1] - 1
                if dist < difference: difference = dist

    for abrick in ghost:
        pygame.draw.rect(ghostSurf, abrick[2], (abrick[0] * 30, (abrick[1]+difference) * 30, 30, 30))
        pygame.draw.rect(ghostSurf, abrick[3], (abrick[0] * 30 + 3, (abrick[1]+difference) * 30 + 3, 24, 24))

    win.blit(ghostSurf, (0, 0))
    drawAll()

    pygame.display.flip()
    clock.tick(30)
