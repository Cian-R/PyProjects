import pygame

pygame.init()
fonts = pygame.font.get_fonts()


class Renderer():
    def __init__(self, screen, clockspeed):
        self.screen = screen
        self.counter = 0
        self.clockspeed = clockspeed
        self.textfont = pygame.font.SysFont(fonts[8], 30)

    def reset_counter(self):
        self.counter = 0

    def render_background(self):
        self.screen.fill((0, 0, 0))

    def render_text(self, text):
        for i in range(len(text)):
            if len(text[i]) == 1:
                outline = text[i]
            else:
                outline = "".join(text[i])
            self.screen.blit(self.textfont.render(outline, True, (255, 255, 255)), (0, i * 30))

    def render_cursor(self, pointer):
        self.counter += 1
        if self.counter > self.clockspeed: self.reset_counter()
        if (self.counter/self.clockspeed) < 0.5:
            pygame.draw.rect(self.screen, (255, 255, 255), ((pointer[1] * 17), (pointer[0] * 30) + 2, 2, 24))


    def render(self, text, pointer):
        self.render_background()
        self.render_text(text)
        self.render_cursor(pointer)


class Data():
    def __init__(self, path):
        self.path = path
        self.data = self.openFile(self.path)
        print("Data:\n", self.data)
        line_pointer = len(self.data) - 1
        char_pointer = len(self.data[-1])
        self.pointer = [line_pointer, char_pointer]
        self.depth = char_pointer

    @staticmethod
    def openFile(path):
        try:
            with open(path, 'r') as file:
                return [x[:-1] for x in file.readlines()]
        except (FileExistsError, FileNotFoundError):
            return [""]

    def writeFile(self, path):
        try:
            file = open(path, 'w')
        except FileNotFoundError:
            file = open(path, 'x')
        for line in self.data:
            file.write(line + "\n")
        file.close()

    def handleKey(self, event):
        x, y = self.pointer
        if event.key == pygame.K_UP:
            if self.pointer[0] == 0:
                self.pointer = [0, 0]
            else:
                self.pointer[0] = self.pointer[0]-1
                if not (len(self.data[self.pointer[0]]) >= self.depth):
                    self.pointer[1] = len(self.data[self.pointer[0]])
                else:
                    self.pointer[1] = self.depth
        elif event.key == pygame.K_DOWN:
            if self.pointer[0] == len(self.data)-1:
                self.pointer[1] = len(self.data[-1])
                self.depth = self.pointer[1]
            else:
                self.pointer[0] += 1
                if not (len(self.data[self.pointer[0]]) >= self.depth):
                    self.pointer[1] = len(self.data[self.pointer[0]])
                else:
                    self.pointer[1] = self.depth
        elif event.key == pygame.K_LEFT:
            if self.pointer[1] != 0:
                self.pointer[1] -= 1
            else:
                if x != 0:
                    self.pointer = [self.pointer[0]-1, len(self.data[self.pointer[0]-1])]
            self.depth = self.pointer[1]
        elif event.key == pygame.K_RIGHT:
            if y != len(self.data[x]):
                self.pointer[1] += 1
            else:
                if x != len(self.data)-1:
                    self.pointer = [x + 1, 0]
            self.depth = self.pointer[1]
        # ===============================================================================
        elif event.key == pygame.K_RETURN:
            modified_data = []
            for index, line in enumerate(self.data):
                if index == x:
                    modified_data.append(line[:y])
                    modified_data.append(line[y:])
                else:
                    modified_data.append(line)
            self.data = modified_data
            self.pointer = [x+1, 0]
            self.depth = self.pointer[1]
        elif event.key == pygame.K_DELETE:
            if not ((x == (len(self.data)-1)) and (y == len(self.data[x]))):
                if y == len(self.data[x]):
                    self.data[x] = "".join(self.data[x:x+2])
                    del self.data[x+1]
                else:
                    self.data[x] = self.data[x][:y] + self.data[x][y+1:]
                self.depth = self.pointer[1]
        elif event.key == pygame.K_BACKSPACE:
            if not ((x == 0) and (y == 0)):
                if y == 0:
                    self.pointer = [x - 1, len(self.data[x - 1])]
                    self.data[x-1] = "".join(self.data[x-1:x+1])
                    del self.data[x]
                else:
                    self.data[x] = self.data[x][:y-1] + self.data[x][y:]
                    self.pointer[1] -= 1
                self.depth = self.pointer[1]
        # ===============================================================================
        elif event.unicode != '':
            self.data[x] = self.data[x][:y] + event.unicode + self.data[x][y:]
            self.pointer[1] += 1
            self.depth = self.pointer[1]


if __name__ == '__main__':
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Notepad")
    completed = False
    clockspeed = 30
    renderer = Renderer(screen, clockspeed)
    data = Data("text_file.txt")
    held_event = [int(clockspeed/2), None]
    while not completed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                completed = True
            elif event.type == pygame.KEYDOWN:
                data.handleKey(event)
                held_event = [int(clockspeed/2), event]
                renderer.reset_counter()
            elif (event.type == pygame.KEYUP) and (held_event[1] is not None):
                if event.key == held_event[1].key:
                    held_event = [int(clockspeed/2), None]
        if type(held_event[1]) == pygame.event.Event:
            if held_event[0] == 0:
                # noinspection PyTypeChecker
                data.handleKey(held_event[1])
                renderer.reset_counter()
            else:
                held_event[0] -= 1


        renderer.render(data.data, data.pointer)
        pygame.display.flip()
        clock.tick(clockspeed)

    data.writeFile("text_file.txt")