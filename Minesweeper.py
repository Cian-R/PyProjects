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
            except: pass
    return count


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def button(screen, msg, x, y, w, h, ic, ac, action=None):
    bmouse = pygame.mouse.get_pos()
    bclick = pygame.mouse.get_pressed()
    if x+w > bmouse[0] > x and y+h > bmouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if (bclick[0] == 1) and (action is not None):
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)


def valbutton(screen, msg, x, y, w, h, ic, ac, val):
    vmouse = pygame.mouse.get_pos()
    vclick = pygame.mouse.get_pressed()
    if x+w > vmouse[0] > x and y+h > vmouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if vclick[0] == 1:
            return val
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (int(x+(w/2)), int(y+(h/2)))
    screen.blit(textSurf, textRect)
    return 0


pygame.init()
bg_colour = (115, 49, 72)

pygame.font.init()
titlefont = pygame.font.SysFont('lucidaconsole', 70)
selecfont = pygame.font.SysFont('lucidaconsole', 20)
bfont = pygame.font.SysFont('lucidaconsole', 40)

win = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Minesweeper')
clock = pygame.time.Clock()

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////// Setup Screen ///////////////////////////////////////////////////
size = 10
mines = 10
board = []
overlay = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # ==================== GRAPHICS DRAWING ====================
    win.fill(bg_colour)
    win.blit(titlefont.render('Minesweeper', False, (255, 255, 255)), (180, 30))
    # Board Size selection buttons.
    win.blit(selecfont.render('Select Board Size:', False, (255, 255, 255)), (40, 220))
    size += valbutton(win, "^", 360, 195, 30, 30, (255, 255, 255), (155, 155, 155), 1)
    size += valbutton(win, "v", 360, 235, 30, 30, (255, 255, 255), (155, 155, 155), -1)
    if size < 10: size = 10
    if size > 30: size = 30
    pygame.draw.rect(win, (115, 20, 20), (260, 195, 90, 70))
    win.blit(titlefont.render(str(size), False, (255, 255, 255)), (265, 200))
    # No of Mines selection buttons.
    win.blit(selecfont.render('Select No. of Mines:', False, (255, 255, 255)), (14, 420))
    mines += valbutton(win, "^", 360, 395, 30, 30, (255, 255, 255), (155, 155, 155), 1)
    mines += valbutton(win, "v", 360, 435, 30, 30, (255, 255, 255), (155, 155, 155), -1)
    if mines < 0: mines = 0
    if mines > 50: mines = 50
    pygame.draw.rect(win, (115, 20, 20), (260, 395, 90, 70))
    win.blit(titlefont.render(str(mines), False, (255, 255, 255)), (265, 400))
    # Continue button
    if valbutton(win, "Go!", 650, 500, 100, 50, (50, 150, 50), (100, 200, 100), 1) == 1:
        break
    pygame.display.update()
    clock.tick(15)

# Create Board
for i in range(size):
    insert = []
    insertoverlay = []
    for e in range(size):
        insert.append(0)
        insertoverlay.append("?")
    board.append(insert)
    overlay.append(insertoverlay)

# Insert Mines
for tick in range(mines):
    a = randint(0, (size - 1))
    b = randint(0, (size - 1))
    while board[a][b] == 9:
        a = randint(0, (size - 1))
        b = randint(0, (size - 1))
    board[a][b] = 9

# Assign Proximity Values
for xval in range(len(board)):
    for yval in range(len(board[xval])):
        if board[xval][yval] != 9:
            board[xval][yval] = VarProxSearch(board, xval, yval, 1, 9)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////// Main Game Loop //////////////////////////////////////////////////
win = pygame.display.set_mode((size*50+20, size*50+20))
mousedown = False
flagcount = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # ==================== GRAPHICS DRAWING ====================
    win.fill((190, 190, 190))
    for row in range(len(board)):
        for square in range(len(board[row])):
            pygame.draw.rect(win, (100, 100, 100), ((10 + square * 50), (10 + row * 50), 50, 50))
            if overlay[row][square] == "?":
                pygame.draw.rect(win, (170, 170, 170), ((15 + square * 50), (15 + row * 50), 40, 40))
            elif overlay[row][square] == "!":
                pygame.draw.rect(win, (204, 157, 47), ((15 + square * 50), (15 + row * 50), 40, 40))
            else:
                pygame.draw.rect(win, (140, 140, 140), ((15 + square * 50), (15 + row * 50), 40, 40))
                if board[row][square] != 0:
                    if board[row][square] != 9:
                        win.blit(bfont.render(str(board[row][square]), False, (255, 255, 255)), ((square*50+22), (row*50+16)))
                    else:
                        pygame.draw.rect(win, (219, 44, 24), (square * 50 + 30, 50 * row + 15, 10, 40))
                        pygame.draw.rect(win, (219, 44, 24), (square * 50 + 15, 50 * row + 30, 40, 10))
                # else: pygame.draw.rect(win, (200, 200, 200), ((15 + square * 50), (15 + row * 50), 40, 40))

    # ==================== Mouse Events ====================
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    mx, my = int((mouse[0] - 10) / 50), int((mouse[1] - 10) / 50)
    # Resetting click
    if (click[0] == 0) and (click[2] == 0) and (mousedown is True):
        mousedown = False
    # Right-click flag toggle
    elif (click[2] == 1) and (mousedown is False):
        mousedown = True
        if overlay[my][mx] == "?":
            overlay[my][mx] = "!"
            flagcount += 1
        elif overlay[my][mx] == "!":
            overlay[my][mx] = "?"
            flagcount -= 1
    # Left-click reveal square
    elif (click[0] == 1) and (mousedown is False):
        mousedown = True
        if overlay[my][mx] == "?": overlay[my][mx] = "."
        if board[my][mx] == 9:
            for t in range(len(overlay)):
                for s in range(len(overlay[t])):
                    overlay[t][s] = "."

        effectrange = [-1, 0, 1]
        row, square = 0, 0
        while (row != size) and (square != size):
            if (overlay[row][square] == ".") and (board[row][square] == 0):
                if VarProxSearch(overlay, row, square, 1, "?") > 0:
                    for a in effectrange:
                        for b in effectrange:
                            if (0 <= row+b < size) and (0 <= square+a < size):
                                try: overlay[row+b][square+a] = "."
                                except: pass
                    row, square = 0, 0
                else: square += 1
            else: square += 1

            if square == size:
                row += 1
                square = 0

    # =========================================================
    pygame.display.update()
    # ==================== Endgame Checks ====================
    if flagcount == mines:
        if "?" not in sum(overlay, []):
            break
    clock.tick(20)

print("you win lmao")
exit()
