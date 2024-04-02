import json
import time
import pygame

pygame.init()
fonts = pygame.font.get_fonts()


class ScrollableList():
    def __init__(self, dictionary_name, list_dictionary):
        self.dictionary_name = dictionary_name
        self.dictionary = list_dictionary
        self.dictionary["Add new entry"] = ""
        self.listfont = pygame.font.SysFont(fonts[8], 20)
        self.mousedown = False
        self.sliding = False

        self.slider_y = 0
        self.sliding_start_y = 0
        self.window_y = 0
        self.mouse_start_y = 0

        self.scrollwindow_size = (50 * len(self.dictionary)) + 10
        self.max_window_y = self.scrollwindow_size - 360
        self.slider_length = int((360 / self.scrollwindow_size) * 400)
        self.max_slider_y = 400 - self.slider_length

        self.highlight_surface = pygame.Surface((300, 40))
        self.highlight_surface.set_alpha(100)
        pygame.draw.rect(self.highlight_surface, (255, 255, 255), (0, 0, 300, 40), border_radius=20)
        print(
            self.slider_length,
            self.scrollwindow_size,
            self.max_slider_y
        )

    def generate_button(self, key, value, count):
        button_surf = pygame.Surface((300, 40))
        button_surf.set_colorkey((255, 0, 255))
        button_surf.fill((255, 0, 255))

        offset = (400 + 20 + 10, 0 + 20 + 10 + (50 * count) - self.window_y)
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = tuple(mouse_pos[i] - offset[i] for i in range(len(mouse_pos)))
        if button_surf.get_rect().collidepoint(relative_mouse_pos):
            pygame.draw.rect(button_surf, (140, 140, 140), (0, 0, 300, 40), border_radius=20)
            if pygame.mouse.get_pressed()[0]:
                print("CLicked:", mouse_pos, offset)
                return button_surf, True
        else:
            pygame.draw.rect(button_surf, (100, 100, 100), (0, 0, 300, 40), border_radius=20)

        if self.dictionary_name == "all":
            button_surf.blit(self.listfont.render(str(key) + " (" + self.dictionary_name + ")",
                                                  False, (0, 0, 0)), (10, 10))
        else:
            button_surf.blit(self.listfont.render(str(key), False, (0, 0, 0)), (10, 10))
        button_surf.blit(self.listfont.render(str(value), False, (0, 0, 0)), (200, 10))


        return button_surf, False

    def generate_slider(self):
        slider_surf = pygame.Surface((20, 400))
        slider_surf.fill((50, 50, 50))
        mouse_pos = pygame.mouse.get_pos()


        if not self.mousedown and pygame.mouse.get_pressed()[0]:
            offset = (400 + 380, 0)
            relative_mouse_pos = tuple(mouse_pos[i] - offset[i] for i in range(len(mouse_pos)))
            if slider_surf.get_rect().collidepoint(relative_mouse_pos):
                self.slider_y = mouse_pos[1] - int(self.slider_length / 2)
                self.sliding = True
                self.mousedown = True
                self.mouse_start_y = mouse_pos[1]
                self.sliding_start_y = self.slider_y

        if self.sliding and not self.mousedown:
            self.sliding = False

        if self.sliding:
            difference = mouse_pos[1] - self.mouse_start_y
            self.slider_y = self.sliding_start_y + difference
        else:
            wheel_direction = 0
            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL:
                    wheel_direction = event.y
            self.slider_y -= 20 * wheel_direction

        if self.slider_y < 0: self.slider_y = 0
        if self.slider_y > 400 - self.slider_length: self.slider_y = 400 - self.slider_length

        pygame.draw.rect(slider_surf, (50, 50, 200), (0, self.slider_y, 20, self.slider_length))
        # print(self.slider_y, self.max_slider_y)
        return slider_surf

    def generate_surface(self, master_surface):
        num_items = len(self.dictionary)
        activated_button = None

        if self.mousedown and not pygame.mouse.get_pressed()[0]:
            self.mousedown = False

        full_surf = pygame.Surface((400, 400))
        scrolling_window = pygame.Surface((320, 360))  # Mask for the scrollable area viewport.
        scrolling_surf = pygame.Surface((320, self.scrollwindow_size))  # Full scrollable area surface.
        scrolling_surf.fill((30, 100, 30))
        count = 0
        for key, value in self.dictionary.items():
            button, activated = self.generate_button(key, value, count)
            scrolling_surf.blit(button, (10, 10 + (50 * count)))
            count += 1
            if activated and not self.mousedown:
                print("Clicking", key, value)
                self.mousedown = True
                activated_button = [key, value]

        if num_items > 7:
            full_surf.blit(self.generate_slider(), (380, 0))

        # Math for scroll window position, from scroll_y/max_scroll_y = window_y/max_window_y
        self.window_y = int((self.slider_y * self.max_window_y)/self.max_slider_y)
        scrolling_window.blit(scrolling_surf, (0, 0 - self.window_y))

        full_surf.blit(scrolling_window, (20, 20))
        master_surface.blit(full_surf, (400, 0))
        return activated_button


class PopupDataEntry():
    def __init__(self, key, item):
        self.keyname = key
        self.itemname = item

    def renderBlackout(self, master_surface):
        blackout_surf = pygame.Surface((800, 400))
        blackout_surf.set_alpha(170)
        blackout_surf.fill((0, 0, 0))
        master_surface.blit(blackout_surf, (0, 0))

    def renderBox(self, master_surface):
        box_surface = pygame.Surface((400, 200))
        pygame.draw.rect(box_surface, (255, 50, 50), (0, 0, 400, 200))

        master_surface.blit(box_surface, (200, 100))



class Data():
    def __init__(self, path):
        self.path = path
        file = open(path, 'r')
        self.dataDic = json.load(file)

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
        self.overlay = None

        self.data = Data(datafile)
        self.focusIndex = 0
        self.focusKey = self.data.get_categories()[self.focusIndex]

        self.scroll_area = ScrollableList(self.focusKey, self.data.returnSubDic(self.focusKey))


    def update(self):
        self.screen.fill((200, 200, 200))

        returned_button = self.scroll_area.generate_surface(self.screen)
        if returned_button:
            print("==========================")
            self.overlay = PopupDataEntry(*returned_button)

        self.drawTotal()

        if self.overlay:
            self.overlay.renderBlackout(self.screen)
            self.overlay.renderBox(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    def drawTotal(self):
        pass

    # def drawList(self):
    #     listwindow = pygame.Surface((400, 400))
    #     categories = self.data.get_categories()
    #     listItems = self.data.returnSubDic(categories[self.focusIndex])
    #
    #     count = 0
    #     for key, value in listItems.items():
    #         pygame.draw.rect(listwindow, (90, 90, 90), (10, 10 + count * 60, 300, 50), border_radius=10)
    #         listwindow.blit(self.listfont.render(str(key), False, (0, 0, 0)), (20, 25 + count * 60))
    #         listwindow.blit(self.listfont.render(str(value), False, (0, 0, 0)), (100, 25 + count * 60))
    #
    #         count += 1
    #
    #     self.screen.blit(listwindow, (400, 0))

    def drawSubWindow(self):
        pass

    def writeData(self):
        json_object = json.dumps(self.data.dataDic, indent=4)
        save_file = open('output.json', 'w')
        save_file.write(json_object)
        save_file.close()
        exit()


if __name__ == '__main__':
    complete = False
    MainUI = BillBotUI('output.json')

    while not complete:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                complete = True
        MainUI.update()
        # print("\n\n\n\n\n\n\n\n")
        # time.sleep(1)

    MainUI.writeData()
