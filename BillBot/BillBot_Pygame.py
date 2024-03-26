import time
import pygame

pygame.init()
fonts = pygame.font.get_fonts()


class ScrollableList():
    def __init__(self, list_dictionary):
        self.dictionary = list_dictionary
        self.mousedown = False
        self.sliding = False
        self.current_y = 0
        self.sliding_start_y = 0
        self.mouse_start_y = 0
        self.listfont = pygame.font.SysFont(fonts[8], 20)

        self.slider_length = 60
        self.max_slider_y = 400 - self.slider_length

        self.highlight_surface = pygame.Surface((300, 40))
        self.highlight_surface.set_alpha(100)
        pygame.draw.rect(self.highlight_surface, (255, 255, 255), (0, 0, 300, 40), border_radius=20)


    def generate_button(self, key, value, count):
        button_surf = pygame.Surface((300, 40))
        pygame.draw.rect(button_surf, (100, 100, 100), (0, 0, 300, 40), border_radius=20)
        button_surf.blit(self.listfont.render(str(key), False, (0, 0, 0)), (10, 10))
        button_surf.blit(self.listfont.render(str(value), False, (0, 0, 0)), (200, 10))

        offset = (400 + 25 + 10, 0 + 25 + 10 + (50 * count))
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = tuple(mouse_pos[i] - offset[i] for i in range(len(mouse_pos)))
        if button_surf.get_rect().collidepoint(relative_mouse_pos):
            button_surf.blit(self.highlight_surface, (0, 0))
            if pygame.mouse.get_pressed()[0]:
                return button_surf, True
        return button_surf, False
    
    def generate_slider(self):
        slider_surf = pygame.Surface((20, 400))
        slider_surf.fill((50, 50, 50))
        mouse_pos = pygame.mouse.get_pos()
        
        if not self.mousedown and pygame.mouse.get_pressed()[0]:
            offset = (400 + 380, 0)
            relative_mouse_pos = tuple(mouse_pos[i] - offset[i] for i in range(len(mouse_pos)))
            if slider_surf.get_rect().collidepoint(relative_mouse_pos):
                self.current_y = mouse_pos[1] - int(self.slider_length/2)
                self.sliding = True
                self.mousedown = True
                self.mouse_start_y = mouse_pos[1]
                self.sliding_start_y = self.current_y
        
        if self.sliding and not self.mousedown:
            self.sliding = False
        
        if self.sliding:
            difference = mouse_pos[1] - self.mouse_start_y
            self.current_y = self.sliding_start_y + difference
        if self.current_y < 0: self.current_y = 0
        if self.current_y > 400-self.slider_length: self.current_y = 400-self.slider_length
            
        
        pygame.draw.rect(slider_surf, (50, 50, 200), (0, self.current_y, 20, self.slider_length))
        print(self.current_y, self.max_slider_y)
        return slider_surf

    def generate_surface(self):
        if self.mousedown and not pygame.mouse.get_pressed()[0]:
            self.mousedown = False

        full_surf = pygame.Surface((400, 400))
        scrolling_window = pygame.Surface((340, 360))
        scrolling_surf = pygame.Surface((340, 700))
        scrolling_surf.fill((30, 100, 30))
        count = 0
        for key, value in self.dictionary.items():
            button, activated = self.generate_button(key, value, count)
            scrolling_surf.blit(button, (10, 10 + (50 * count)))
            count += 1
            if activated and not self.mousedown:
                self.mousedown = True
                print("Clicking", key, value)
        
        full_surf.blit(self.generate_slider(), (380, 0))

        scrolling_window.blit(scrolling_surf, (0, 0 - self.current_y))
        full_surf.blit(scrolling_window, (20, 20))
        return full_surf



class Data():
    def __init__(self, path):
        self.path = path
        self.dataDic = {
            "all": {
                'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26
            },
            "first": {

            }}

    def returnSubDic(self, subset):
        return self.dataDic[subset]

    def add_category(self, category_name):
        self.dataDic[category_name] = {}

    def add_item(self, category, item, value):
        self.dataDic["all"][item] = value
        self.dataDic[category][item] = value

    def tree(self):
        for item in self.dataDic.keys():
            print("+", item)
            for line in self.dataDic[item].keys():
                print("    -", line, self.dataDic[item][line])

    def get_categories(self):
        return [name for name in self.dataDic.keys()]

    def get_items(self, cat):
        return [item for item in self.dataDic[cat].keys()]

    def remove_category(self, cat):
        for key in self.dataDic[cat].keys():
            del self.dataDic["all"][key]
        del self.dataDic[cat]


class BillBotUI():
    def __init__(self, datafile):
        pygame.display.set_caption("BillBot")
        # window_icon = pygame.image.load('src/icon.png')
        # pygame.display.set_icon(window_icon)
        self.screen = pygame.display.set_mode((800, 400))
        self.clock = pygame.time.Clock()
        self.listfont = pygame.font.SysFont(fonts[8], 20)

        self.data = Data(datafile)
        self.focusIndex = 0
        self.focusKey = self.data.get_categories()[self.focusIndex]

        self.scroll_area = ScrollableList(self.data.returnSubDic(self.focusKey))

        self.subWindow = False



    def update(self):
        if self.subWindow:
            self.drawSubWindow()
        else:
            self.screen.fill((200, 200, 200))
            list_surf = self.scroll_area.generate_surface()
            self.screen.blit(list_surf, (400, 0))
            self.drawTotal()
        pygame.display.flip()
        self.clock.tick(30)

    def drawTotal(self):
        pass

    def drawList(self):
        listwindow = pygame.Surface((400, 400))
        categories = self.data.get_categories()
        listItems = self.data.returnSubDic(categories[self.focusIndex])

        count = 0
        for key, value in listItems.items():
            pygame.draw.rect(listwindow, (90, 90, 90), (10, 10 + count * 60, 300, 50), border_radius=10)
            listwindow.blit(self.listfont.render(str(key), False, (0, 0, 0)), (20, 25 + count * 60))
            listwindow.blit(self.listfont.render(str(value), False, (0, 0, 0)), (100, 25 + count * 60))

            count += 1

        self.screen.blit(listwindow, (400, 0))

    def drawSubWindow(self):
        pass

    def writeData(self):
        pass


if __name__ == '__main__':
    complete = False
    MainUI = BillBotUI('src/datafile.txt')

    while not complete:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                complete = True
        MainUI.update()
        # print("\n\n\n\n\n\n\n\n")
        # time.sleep(1)

    MainUI.writeData()
