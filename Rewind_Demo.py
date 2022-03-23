import pygame
import math

pygame.init()
cl_black = (0, 0, 0)

pygame.font.init()
titlefont = pygame.font.SysFont('inkfree', 70)

win = pygame.display.set_mode((1600, 800))
pygame.display.set_caption('Rewind')
clock = pygame.time.Clock()

timemod = 3
player = [700, 200]
enemy = [200, 400]
history = []
hspeed = 0
vspeed = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: hspeed -= 1
            if event.key == pygame.K_d: hspeed += 1
            if event.key == pygame.K_w: vspeed -= 1
            if event.key == pygame.K_s: vspeed += 1
            if event.key == pygame.K_j:
                if len(history) == 30*timemod:
                    player[0] = history[0][0]
                    player[1] = history[0][1]
                    history = []
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: hspeed += 1
            if event.key == pygame.K_d: hspeed -= 1
            if event.key == pygame.K_w: vspeed += 1
            if event.key == pygame.K_s: vspeed -= 1

    win.fill(cl_black)
    history.append([player[0], player[1]])
    for i in range(len(history)):
        pygame.draw.rect(win, (80, 40, 40), (history[i][0] + 18, history[i][1] + 18, 4, 4))
    if len(history) > 30 * timemod:
        del history[0]

        pygame.draw.rect(win, (80, 40, 40), (history[0][0], history[0][1], 40, 40))
    player[0] = player[0] + (10 * hspeed)
    player[1] = player[1] + (10 * vspeed)

    if math.dist(player, enemy) < 150:
        enemy[1] = enemy[1] - 11

    pygame.draw.rect(win, (200, 100, 100), (player[0], player[1], 40, 40))
    pygame.draw.rect(win, (100, 200, 100), (enemy[0], enemy[1], 40, 40))

    pygame.draw.rect(win, (50, 50, 50), (10, 10, 360, 50))
    pygame.draw.rect(win, (80, 80, 80), (10, 10, 4*len(history), 50))

    pygame.display.update()
    clock.tick(30)
