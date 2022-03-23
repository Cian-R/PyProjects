import pygame

pygame.init()
fonts = pygame.font.get_fonts()
win = pygame.display.set_mode((1200, 600))

index = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: index -= 1
            elif event.key == pygame.K_RIGHT: index += 1

    win.fill((255, 255, 255))
    myfont = pygame.font.SysFont(fonts[index], 100)
    win.blit(myfont.render(str(fonts[index]), False, (0, 0, 0)), (100, 100))

    pygame.display.update()
