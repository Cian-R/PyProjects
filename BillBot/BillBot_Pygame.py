import pygame

pygame.init()


class Data():
    def __init__(self, path):
        self.path = path
        self.dataDic = {"all": {1: 2}}

    def returnList(self, subset):
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

        self.data = Data(datafile)
        self.focusIndex = 0

        self.subWindow = False



    def update(self):
        if self.subWindow:
            self.drawSubWindow()
        else:
            self.screen.fill((200, 200, 200))
            self.drawList()
            self.drawTotal()
        pygame.display.flip()

    def drawTotal(self):
        pass

    def drawList(self):
        listwindow = pygame.Surface((400, 400))
        categories = self.data.get_categories()
        target = categories[self.focusIndex]
        self._drawListItems(listwindow, target, 0)
        self.screen.blit(listwindow, (400, 0))

    def drawSubWindow(self):
        pass

    def writeData(self):
        pass

    def _drawListItems(self, surf, cat, index):
        pygame.draw.rect(surf, (30, 30, 30), (10, 10 + index*30, 50, 20))


        if index > len(self.data.get_items(cat)):
            return None
        else:
            return self._drawListItems(surf, cat, index+1)


if __name__ == '__main__':
    complete = False
    MainUI = BillBotUI('src/datafile.txt')

    while not complete:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                complete = True
        MainUI.update()

    MainUI.writeData()
