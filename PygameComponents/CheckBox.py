import pygame


class CheckBox():
    def __init__(self, position, offset, size, rounding, colour=(0, 0, 0), is_active=False):
        self.position = position
        self.offset = offset
        self.size = size
        self.rect = pygame.Rect((position[0], position[1], self.size, self.size))
        self.rounding = rounding
        if type(colour) == pygame.Color:
            self.colour = colour
        else:
            self.colour = pygame.Color(colour)
        self.is_active = is_active
        self.clicking = True


    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        relative_mouse_pos = tuple(mouse_pos[i] - self.offset[i] for i in range(len(mouse_pos)))
        if self.clicking and (not mouse_click):
            self.clicking = False
        if (not self.clicking) and mouse_click:
            self.clicking = True
            if self.rect.collidepoint(relative_mouse_pos):
                self.is_active = not self.is_active
            else:
                self.is_active = False

        return self.is_active


    def draw(self, target_surface):
        pygame.draw.rect(target_surface, self.co)
        