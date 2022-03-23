import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))


s = pygame.Surface((200, 200))  # the size of your rect
s.set_alpha(100)



done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))
    s.fill((255, 255, 255))

    pygame.draw.rect(screen, (200, 0, 0), (150, 150, 100, 100))
    pygame.draw.rect(s, (20, 200, 20), (100, 100, 100, 100))

    screen.blit(s, pygame.mouse.get_pos())
    pygame.display.flip()
