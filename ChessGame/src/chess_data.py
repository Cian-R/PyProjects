import pygame

# pygame.init()
pygame.font.init()
fonts = {  # Potential future use in a UI
    "titlefont": pygame.font.SysFont('lucidaconsole', 70),
    "selecfont": pygame.font.SysFont('lucidaconsole', 20),
    "bfont": pygame.font.SysFont('lucidaconsole', 40)
}

directions = {
    "up": [0, -1],
    "down": [0, 1],
    "left": [-1, 0],
    "right": [1, 0],
    "upleft": [-1, -1],
    "upright": [1, -1],
    "downleft": [-1, 1],
    "downright": [1, 1],
}
knight_directions = {
    "ul": [-2, -1],
    "ur": [-2, 1],
    "dl": [2, -1],
    "dr": [2, 1],
    "lu": [-1, -2],
    "ld": [1, -2],
    "ru": [-1, 2],
    "rd": [1, 2],
}

bg_colour = (100, 100, 100)

whiteSq = (238, 238, 210)
blackSq = (118, 150, 86)

square_sizes = [75, 100, 150]  # For future use, potential for multiple window sizes. Look into spritesheet scaling.
