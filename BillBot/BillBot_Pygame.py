import json
# import time
import pygame


pygame.init()
fonts = pygame.font.get_fonts()


class Button():
    def __init__(self, w, h, colour, offcolour, text, offset):
        self.size = [w, h]
        self.offset = (offset[0], offset[1])
        self.surf = pygame.Surface(self.size)
        self.surf.set_colorkey((255, 0, 255))
        self.surf.fill((255, 0, 255))
        self.colour = colour
        self.offcolour = offcolour
        listfont = pygame.font.SysFont(fonts[8], 20)
        self.text = text
        self.txt_surface = listfont.render(text, True, (0, 0, 0))

    def draw(self, master_surf, position, usable=True):
        fixed_offset = (self.offset[0] + position[0], self.offset[1] + position[1])
        factors = (0, 0, self.size[0], self.size[1])
        if not usable:
            pygame.draw.rect(self.surf, (60, 60, 60), factors, border_radius=10)
        else:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]
            relative_mouse_pos = tuple(mouse_pos[i] - fixed_offset[i] for i in range(len(mouse_pos)))
            if self.surf.get_rect().collidepoint(relative_mouse_pos):
                pygame.draw.rect(self.surf, self.offcolour, factors, border_radius=10)
                pygame.draw.rect(self.surf, self.colour, factors, border_radius=10, width=2)
                if mouse_click:
                    return True
            else:
                pygame.draw.rect(self.surf, self.colour, factors, border_radius=10)
                pygame.draw.rect(self.surf, self.offcolour, factors, border_radius=10, width=2)
        self.surf.blit(self.txt_surface, (10, 12))
        master_surf.blit(self.surf, position)
        return False


class InputBox:
    def __init__(self, x, y, w, h, text='', placeholder='', offset=(0, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = (80, 200, 200)
        self.text = str(text)
        self.listfont = pygame.font.SysFont(fonts[8], 20)
        self.placeholder_txt = self.listfont.render(placeholder, True, (100, 100, 140))
        self.txt_surface = self.listfont.render(self.text, True, self.colour)
        self.active = False
        self.offset = [offset[0], offset[1]]
        self.clicking = True

    def handle_event(self, keyinput):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        offset = (200, 100)
        relative_mouse_pos = tuple(mouse_pos[i] - offset[i] for i in range(len(mouse_pos)))
        if (not self.clicking) and mouse_click:
            self.clicking = True
            if self.rect.collidepoint(relative_mouse_pos):
                self.active = not self.active
            else:
                self.active = False
        if self.clicking and (not mouse_click):
            self.clicking = False
        if self.active:
            if len(keyinput) > 0:
                print(f"box {self.text} recieved key input '{keyinput}'")
                if keyinput == '\b':
                    self.text = self.text[:-1]
                else:
                    self.text += keyinput
                self.txt_surface = self.listfont.render(self.text, True, self.colour)
        return self.text

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (50, 100, 200), self.rect, 2)
        else:
            pygame.draw.rect(screen, (50, 200, 100), self.rect, 2)
        if self.text == '':
            screen.blit(self.placeholder_txt, (self.rect.x + 10, self.rect.y + 10))
        else:
            screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))


class ScrollableList():
    def __init__(self, dictionary_name, list_dictionary):
        self.dictionary_name = dictionary_name
        self.dictionary = list_dictionary
        self.listfont = pygame.font.SysFont(fonts[8], 20)
        self.mousedown = False
        self.sliding = False

        self.slider_y = 0
        self.sliding_start_y = 0
        self.window_y = 0
        self.mouse_start_y = 0

        if self.dictionary_name == "all":
            self.num_items = len(self.dictionary)
        else:
            self.num_items = len(self.dictionary) + 1

        self.scrollwindow_size = (50 * self.num_items) + 10
        self.max_window_y = self.scrollwindow_size - 360
        self.slider_length = int((360 / self.scrollwindow_size) * 400)
        self.max_slider_y = 400 - self.slider_length

        self.highlight_surface = pygame.Surface((300, 40))
        self.highlight_surface.set_alpha(100)
        pygame.draw.rect(self.highlight_surface, (255, 255, 255), (0, 0, 300, 40), border_radius=20)

    def generate_button(self, key, value, count):
        button_surf = pygame.Surface((300, 40))
        button_surf.set_colorkey((255, 0, 255))
        button_surf.fill((255, 0, 255))
        clicked = False

        offset = (400 + 20 + 10, 0 + 20 + 10 + (50 * count) - self.window_y)
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = tuple(mouse_pos[i] - offset[i] for i in range(len(mouse_pos)))
        if button_surf.get_rect().collidepoint(relative_mouse_pos):
            pygame.draw.rect(button_surf, (140, 140, 140), (0, 0, 300, 40), border_radius=20)
            pygame.draw.rect(button_surf, (200, 200, 200), (0, 0, 300, 40), border_radius=20, width=2)
            if pygame.mouse.get_pressed()[0]:
                print("~~Clicked:", mouse_pos, offset)
                clicked = True
        else:
            pygame.draw.rect(button_surf, (100, 100, 100), (0, 0, 300, 40), border_radius=20)

        button_surf.blit(self.listfont.render(str(key), False, (0, 0, 0)), (10, 10))
        button_surf.blit(self.listfont.render(str(value), False, (0, 0, 0)), (200, 10))

        return button_surf, clicked

    def generate_add_button(self, count):
        button_surf = pygame.Surface((300, 40))
        button_surf.set_colorkey((255, 0, 255))
        button_surf.fill((255, 0, 255))
        clicked = False

        offset = (400 + 20 + 10, 0 + 20 + 10 + (50 * count) - self.window_y)
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = tuple(mouse_pos[i] - offset[i] for i in range(len(mouse_pos)))
        if button_surf.get_rect().collidepoint(relative_mouse_pos):
            pygame.draw.rect(button_surf, (100, 100, 100), (0, 0, 300, 40), border_radius=20)
            pygame.draw.rect(button_surf, (160, 160, 160), (0, 0, 300, 40), border_radius=20, width=2)
            if pygame.mouse.get_pressed()[0]:
                print("~~Clicked:", mouse_pos, offset)
                clicked = True
        else:
            pygame.draw.rect(button_surf, (60, 60, 60), (0, 0, 300, 40), border_radius=20)

        button_surf.blit(self.listfont.render("Add new entry.", False, (0, 0, 0)), (80, 10))

        return button_surf, clicked

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
            for event in pygame.event.get(eventtype=pygame.MOUSEWHEEL):
                wheel_direction = event.y
            self.slider_y -= 20 * wheel_direction

        if self.slider_y < 0: self.slider_y = 0
        if self.slider_y > 400 - self.slider_length: self.slider_y = 400 - self.slider_length

        pygame.draw.rect(slider_surf, (50, 50, 200), (0, self.slider_y, 20, self.slider_length))
        return slider_surf

    def draw(self, master_surface):

        activated_button = None

        if self.mousedown and not pygame.mouse.get_pressed()[0]:
            self.mousedown = False

        full_surf = pygame.Surface((400, 400))
        scrolling_window = pygame.Surface((320, 360))  # Mask for the scrollable area viewport.
        scrolling_window.fill((255, 0, 255))
        scrolling_window.set_colorkey((255, 0, 255))
        pygame.draw.rect(scrolling_window, (10, 70, 10), (0, 0, 320, 360), border_radius=8)
        scrolling_surf = pygame.Surface((320, self.scrollwindow_size))  # Full scrollable area surface.
        scrolling_surf.fill((255, 0, 255))
        scrolling_surf.set_colorkey((255, 0, 255))
        count = 0
        for key, value in self.dictionary.items():
            button, activated = self.generate_button(key, value, count)
            scrolling_surf.blit(button, (10, 10 + (50 * count)))
            count += 1
            if activated and not self.mousedown:
                print("Clicking", key, value)
                self.mousedown = True
                activated_button = [key, value]
        if self.dictionary_name != "all":
            button, activated = self.generate_add_button(count)
            scrolling_surf.blit(button, (10, 10 + (50 * count)))
            if activated and not self.mousedown:
                print("Clicking", "", "")
                self.mousedown = True
                activated_button = ["", ""]

        if self.num_items > 7:
            full_surf.blit(self.generate_slider(), (380, 0))
            self.window_y = int((self.slider_y * self.max_window_y) / self.max_slider_y)
        scrolling_window.blit(scrolling_surf, (0, 0 - self.window_y))

        full_surf.blit(scrolling_window, (20, 20))
        master_surface.blit(full_surf, (400, 0))
        return activated_button


class TotalView():
    def __init__(self, dataDic, categories, starting_index):
        self.listfont = pygame.font.SysFont(fonts[8], 10)
        self.grandfont = pygame.font.SysFont(fonts[69], 40)
        self.mousedown = False

        self.dataDic = dataDic
        self.categories = categories
        self.selected_index = starting_index
        self.selected_category = self.categories[self.selected_index]
        self.create_button = Button(200, 40, (200, 100, 50), (150, 50, 10), "Create Category", (5, 5))
        self.delete_button = Button(200, 40, (200, 30, 30), (100, 10, 10), "Delete Category", (5, 5))

    def draw(self, master_surface):
        main_view = pygame.Surface((400, 400))
        main_view.fill((230, 140, 40))
        view_box = pygame.Surface((390, 390))

        return_code = 0
        return_value = None

        taboffset = 0
        delay = False
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if (not click) and self.mousedown:
            self.mousedown = False

        for tab in range(len(self.categories)):
            txt_surface = self.listfont.render(str(self.categories[tab]).upper(), True, (0, 0, 0))
            width = txt_surface.get_width() + 10
            if self.categories[tab] == self.selected_category:
                pygame.draw.rect(view_box, (215, 215, 215), (0 + taboffset, 0, width, 50), border_radius=4)
                delay = True
            else:
                pygame.draw.rect(view_box, (150, 150, 150), (0 + taboffset, 5, width, 45), border_radius=4)
                if tab != 0:
                    if not delay:
                        pygame.draw.line(view_box, (20, 20, 20), (0 + taboffset, 15), (0 + taboffset, 35), 1)
                    else:
                        delay = False
            offset = (5 + taboffset, 20)
            if (offset[0] < mouse_pos[0] < (offset[0] + width)) and (offset[1] < mouse_pos[1] < (offset[1] + 25)):
                if (not self.mousedown) and pygame.mouse.get_pressed()[0]:
                    self.mousedown = True
                    self.selected_index = tab
                    self.selected_category = self.categories[self.selected_index]
                    return_code, return_value = 1, self.selected_category

            view_box.blit(txt_surface, (5 + taboffset, 20))

            taboffset += width

        pygame.draw.rect(view_box, (215, 215, 215), (0, 40, 390, 260), border_radius=10)

        total = 0
        for value in self.dataDic[self.selected_category].values():
            total += float(value)
        outstring = str(total)
        if len(outstring.split()) > 1:
            if len(outstring.split(".")[1]) == 1:
                outstring = outstring + "0"
        view_box.blit(self.grandfont.render(f"${outstring} / month", False, (0, 0, 0)), (30, 100))

        can_delete = (self.selected_category != "all")
        if self.create_button.draw(view_box, (50, 300)):
            return_code, return_value = 2, None
        if self.delete_button.draw(view_box, (50, 350), usable=can_delete):
            return_code, return_value = 3, self.selected_category

        main_view.blit(view_box, (5, 5))
        master_surface.blit(main_view, (0, 0))

        return return_code, return_value


class PopupDataEntry():
    def __init__(self, key, value):
        self.keyname = key
        self.old_keyname = key
        self.value = value
        self.old_value = value
        self.listfont = pygame.font.SysFont(fonts[8], 20)

        self.keybox = InputBox(20, 20, 360, 40, text=self.keyname, placeholder='Title', offset=(200, 100))
        self.valuebox = InputBox(20, 80, 360, 40, text=self.value, placeholder='$ Cost / Month', offset=(200, 100))

        self.cancelbutton = Button(100, 40, (200, 100, 100), (250, 150, 150), "Cancel", (200, 100))
        if self.old_keyname != "":
            self.deletebutton = Button(100, 40, (200, 10, 10), (250, 10, 10), "Delete", (200, 100))
        self.confirmbutton = Button(100, 40, (100, 200, 100), (150, 250, 150), "Confirm", (200, 100))

    @staticmethod
    def renderBlackout(master_surface):
        blackout_surf = pygame.Surface((800, 400))
        blackout_surf.set_alpha(170)
        blackout_surf.fill((0, 0, 0))
        master_surface.blit(blackout_surf, (0, 0))

    def renderBox(self, master_surface, keyinput):
        self.keyname = self.keybox.handle_event(keyinput)
        self.value = self.valuebox.handle_event(keyinput)

        box_surface = pygame.Surface((400, 200))
        pygame.draw.rect(box_surface, (50, 50, 100), (0, 0, 400, 200))

        self.keybox.draw(box_surface)
        self.valuebox.draw(box_surface)

        if self.cancelbutton.draw(box_surface, (20, 140)):
            print(f'cancel {self.old_keyname} {self.old_value} |')
            return [self.old_keyname, self.old_keyname, self.old_value]

        if (len(self.value) > 0) and (len(self.keyname) > 0):
            try:
                float(self.value)
                can_confirm = True
            except ValueError:
                can_confirm = False
        else:
            can_confirm = False
        if self.confirmbutton.draw(box_surface, (280, 140), usable=can_confirm):
            print(f'confirm {self.keyname} {self.value}')
            return [self.old_keyname, self.keyname, self.value]

        if self.old_keyname != "":
            if self.deletebutton.draw(box_surface, (150, 140)):
                print(f'cancel {self.keyname} {self.value}')
                return [self.old_keyname, "", ""]

        master_surface.blit(box_surface, (200, 100))

        return [False, False, False]


class Data():
    def __init__(self, path):
        self.path = path
        try:
            file = open(path, 'r')
            self.dataDic = json.load(file)
            file.close()
            print(self.dataDic)
        except FileNotFoundError:
            print(f"File {path} doesn't exist. Creating new.")
            file = open(path, 'x')
            file.close()
            self.dataDic = {'all': {}}
        except json.JSONDecodeError:
            print(f"Decode error trying to read contents of {path}")
            print("Enter 'Y' to wipe data of file and treat as new. Enter anything else to close program safely.")
            if input("> ").lower() == 'y':
                print("\nWiping ...")
                file = open(path, 'w')
                file.write("")
                file.close()
                self.dataDic = {'all': {}}
            else:
                print("\nExiting")
                exit()

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

    def remove_item(self, cat, key):
        del self.dataDic[cat][key]


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BillBotUI():
    def __init__(self, datafile):
        self.path = datafile
        self.data = Data(datafile)

        pygame.display.set_caption("BillBot")
        # window_icon = pygame.image.load('src/icon.png')
        # pygame.display.set_icon(window_icon)
        self.screen = pygame.display.set_mode((800, 400))
        self.clock = pygame.time.Clock()
        self.listfont = pygame.font.SysFont(fonts[8], 20)
        self.overlay = None
        self.actionlock = True

        self.focusIndex = 3
        if self.focusIndex > len(self.data.get_categories()) - 1:
            self.focusIndex = 0
        self.focusKey = self.data.get_categories()[self.focusIndex]

        self.scroll_area = ScrollableList(self.focusKey, self.data.returnSubDic(self.focusKey))
        self.totalview = TotalView(self.data.dataDic, self.data.get_categories(), self.focusIndex)

    def activate(self):
        completed = False
        while not completed:
            click = pygame.mouse.get_pressed()[0]
            keyinput = ""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    completed = True
                if event.type == pygame.KEYDOWN:
                    keyinput = str(event.unicode)
            if (not click) and self.actionlock:
                self.actionlock = False
            # ===================================================================================================
            if self.overlay:
                unhook = self.overlay.renderBox(self.screen, keyinput)
                if (unhook[0] is not False) and (not self.actionlock):
                    print(f'UNHOOK COMMAND: {unhook}')
                    if unhook[0] != unhook[1]:
                        print("unhook - change/delete key")
                        self.data.remove_item(self.focusKey, unhook[0])
                    if unhook[1] != "":
                        print("unhook - add/update key")
                        self.data.dataDic[self.focusKey][unhook[1]] = unhook[2]
                    print("unhooking", self.overlay)
                    self.overlay = None
                    print(self.overlay)
                    if unhook[0] != unhook[1]:
                        self.scroll_area = ScrollableList(self.focusKey, self.data.returnSubDic(self.focusKey))
                    self.actionlock = True
            # ===================================================================================================
            else:
                self.screen.fill((200, 200, 200))

                command, command_data = self.totalview.draw(self.screen)
                if command == 1:
                    self.focusKey = command_data
                    self.scroll_area = ScrollableList(self.focusKey, self.data.returnSubDic(self.focusKey))
                elif command == 2:
                    pass
                elif command == 3:
                    self.data.remove_category(command_data)
                    self.focusIndex = 0
                    self.focusKey = self.data.get_categories()[0]
                    self.totalview = TotalView(self.data.dataDic, self.data.get_categories(), self.focusIndex)
                    self.scroll_area = ScrollableList(self.focusKey, self.data.returnSubDic(self.focusKey))

                returned_button = self.scroll_area.draw(self.screen)

                if returned_button and (not self.actionlock):
                    print(f"commencing overlay with {returned_button}")
                    self.overlay = PopupDataEntry(*returned_button)
                    self.overlay.renderBlackout(self.screen)
                    self.actionlock = True

            # if self.actionlock: pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 10, 10))
            pygame.display.flip()
            self.clock.tick(30)
        return None

    def drawSubWindow(self):
        pass

    def writeData(self):
        json_object = json.dumps(self.data.dataDic, indent=4)
        save_file = open(self.path, 'w')
        save_file.write(json_object)
        save_file.close()
        exit()


if __name__ == '__main__':
    complete = False
    MainUI = BillBotUI('src/output.json')
    MainUI.activate()
    MainUI.writeData()
