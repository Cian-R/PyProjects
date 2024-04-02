import time
import copy
import pygame
import random


WHITE = (255, 255, 255)
BLUE = (50, 50, 250)
GREEN = (50, 200, 50)
DARK_GREEN = (50, 100, 50)
BLACK = (0, 0, 0)

units = int(input("Num Units     > "))
screen_spacing = 1190/(units-1)
# screen_spacing = 100

people = int(input("Num People    > "))

spacing_value = int(input("Spacing (m)   > "))
tag_range = int(input("Tag Range (m) > "))
real_spacing_index = tag_range / spacing_value

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200, 600))
fonts = pygame.font.get_fonts()
listfont = pygame.font.SysFont(fonts[8], 20)


class Person():
    def __init__(self, id_value):
        self.id = id_value
        self.speed = random.randint(1, 3)
        self.facing = (random.randint(0, 1) * 2) - 1
        self.position = random.randint(0, 1200)

    def update(self):
        self.position = self.position + (self.speed * self.facing)

        if self.position < 0:
            self.position = 0
            self.facing = self.facing * -1

        if self.position > 1200:
            self.position = 1200
            self.facing = self.facing * -1

    def draw(self, surf):
        pygame.draw.circle(surf, GREEN, (self.position, 20), 10)
        surf.blit(listfont.render(str(self.id), False, WHITE), (self.position, 0))


class Dragonfly():
    def __init__(self, id_value):
        self.id = id_value
        self.surface = None
        self.position = None
        self.tags = {}
        self.tagslast = {}
        self.polling = False
        pass

    def unpoll(self):
        self.polling = False

    def draw(self, surface, index):
        self.surface = surface
        self.position = index * screen_spacing

        for key, item in self.tags.items():
            self.tags[key] = [item[0], item[1] + 1]

        if self.polling:
            pygame.draw.circle(self.surface, BLUE, (self.position, 40), 10)
        else:
            pygame.draw.circle(self.surface, WHITE, (self.position, 40), 10)

    def poll(self, people):
        self.polling = True
        self.tagslast = copy.deepcopy(self.tags)
        updates = []
        max_range = screen_spacing * real_spacing_index
        print(f"\nmax {max_range} |  screenspacing {screen_spacing} | real_spacing {real_spacing_index}")
        for person in people:
            distance_to_person = abs(person.position - self.position)
            print(f"distance to {person.id} is {distance_to_person}, max range {max_range}")
            if distance_to_person < max_range:
                print("Inside!")
                updates.append([person.id, self.position])
                self.tags[person.id] = [(1 - (distance_to_person/max_range)), 0]

        print("NOW -> ", self.tags)
        print("OLD -> ", self.tagslast)
        return updates


unit_list = []
for a in range(units):
    unit_list.append(Dragonfly(a))
print(unit_list)

people_list = []
live_positions = []
for b in range(people):
    newperson = Person(b)
    people_list.append(newperson)
    live_positions.append({"id": newperson.id, "x": None, "age": 0})
print(unit_list)



ticker = 0
polled = Dragonfly(99999)
next_poll = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill((0, 0, 0))
    for person in people_list:
        person.update()

    for unit_no in range(len(unit_list)):
        unit_list[unit_no].draw(screen, unit_no)

    for person_no in range(len(people_list)):
        people_list[person_no].draw(screen)

    for person in live_positions:
        person["age"] += 0.5
        if person["x"] is not None:
            pygame.draw.circle(screen, DARK_GREEN, (person["x"], person["age"]), 10)
            screen.blit(listfont.render(str(person["id"]), False, WHITE), (person["x"], person["age"]))
            pygame.draw.line(screen, WHITE, (person["x"], person["age"]), (people_list[person["id"]].position, 30))

    ticker += 1
    if ticker == 60:
        if polled:
            polled.unpoll()
        ticker = 0
        polled = unit_list[next_poll]
        incoming_updates = polled.poll(people_list)
        for pair in incoming_updates:
            for person in live_positions:
                if person["id"] == pair[0]:
                    person["x"] = pair[1]
                    person["age"] = 0

        print("Ghosts:", live_positions)
        next_poll += 1
        if next_poll > units - 1:
            next_poll = 0
    # elif ticker == 2:
    #     time.sleep(10)
    # pygame.draw.rect(screen, (200, 0, 0), (150, 150, 100, 100))

    pygame.display.flip()
    clock.tick(60)
