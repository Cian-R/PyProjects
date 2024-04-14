import pygame


class InputBox:
    """
    Creates a simple free-text input box with variable size
    """
    """
    ...

    Attributes
    ----------
    xywh: tuple
        tuple representing (x_position, y_position, width, height)
        x and y positions are for the target_surf in the draw() method.

    colour: tuple / pygame.Colour
        either a tuple of type (RedValue, GreenValue, BlueValue) where 0 <= value <= 255
        or a pygame.Colour object

    font: pygame.Font
        pygame font object, pygame.font_name.SysFont(font, size)

    text: str
        The font that should already be in the input field, useful if editing a value.
        Default: ""

    placeholder: str
        The placeholder text that is rendered when the box is empty.
        Default: ""

    offset: tuple
        Tuple of type (x, y) where the offset is the position of the target_surface relative to main screen.
        Default: (0, 0)  -  only use default if target_surface = main screen.

    is_active: bool
        True if typing letters will affect this input box.
    """

    def __init__(self, xywh, colour, font, text='', placeholder='', offset=(0, 0), is_active=False):
        self.rect = pygame.Rect(*xywh)
        if type(colour) == pygame.Color:
            self.colour = colour
        else:
            self.colour = pygame.Color(colour)
        
        self.text = str(text)
        self.display_font = font
        self.placeholder_txt = self.display_font.render(placeholder, True, (100, 100, 140))
        self.txt_surface = self.display_font.render(self.text, True, self.colour)
        
        self.is_active = is_active
        self.offset = offset
        self.clicking = True


    def handle_event(self, keyinput):
        # Function returns (display_text, is_tabbed, is_returned)
        #        In format (string,       bool,      bool       )
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        offset = (200, 100)
        relative_mouse_pos = tuple(mouse_pos[i] - offset[i] for i in range(len(mouse_pos)))
        if self.clicking and (not mouse_click):
            self.clicking = False
        if (not self.clicking) and mouse_click:
            self.clicking = True
            if self.rect.collidepoint(relative_mouse_pos):
                self.is_active = not self.is_active
            else:
                self.is_active = False
        
        if self.is_active:
            if len(keyinput) > 0:
                print(f"box {self.text} recieved key input! |{keyinput}|")
                if keyinput == '\b':
                    self.text = self.text[:-1]
                elif keyinput == '	':
                    return self.text, True, False
                elif keyinput == '\r':
                    return self.text, False, True
                else:
                    self.text += keyinput
                self.txt_surface = self.display_font.render(self.text, True, self.colour)
        return self.text, False, False
    

    def draw(self, target_surface):
        if self.is_active:
            pygame.draw.rect(target_surface, (50, 100, 200), self.rect, 2)
        else:
            pygame.draw.rect(target_surface, (50, 200, 100), self.rect, 2)
        if self.text == '':
            target_surface.blit(self.placeholder_txt, (self.rect.x + 10, self.rect.y + 10))
        else:
            target_surface.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
