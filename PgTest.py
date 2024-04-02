import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))


s = pygame.Surface((200, 200))  # the size of your rect
s.set_alpha(100)

test_s = pygame.Surface((400, 50))  # the size of your rect



done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((50, 50, 50))
    s.fill((255, 255, 255))

    pygame.draw.rect(screen, (200, 0, 0), (150, 150, 100, 100))
    pygame.draw.rect(s, (20, 200, 20), (100, 100, 100, 100))

    pygame.draw.rect(test_s, (0, 0, 200), (0, 0, 50, 50))

    screen.blit(test_s, (0, 0))
    screen.blit(s, pygame.mouse.get_pos())
    pygame.display.flip()
