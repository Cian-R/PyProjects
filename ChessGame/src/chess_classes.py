import pygame
import json
from chess_data import blackSq, whiteSq


class Square:
    def __init__(self, colour, coords):
        if colour:
            self.colour = whiteSq
        else:
            self.colour = blackSq
        self.piece = None
        self.coords = coords
        self.truepos = [10 + (coords[0] * 75), 10 + (coords[1] * 75)]
        self.highlighted = False
        self.marked = False

    def __str__(self):
        if self.piece:
            return f"<<Square - {self.piece.get_name()}>> {str(self.piece)} {str(self.coords)}"
        else:
            return f"<<Square>> {str(self.piece)} {str(self.coords)}"

    def __repr__(self): return str(self.colour) + str(self.piece) + str(self.coords)

    def draw(self, surf):
        pygame.draw.rect(surf, self.colour, (self.truepos[0], self.truepos[1], 75, 75))

        if self.highlighted:
            highlight = pygame.Surface((75, 75))
            highlight.set_alpha(128)
            highlight.fill((200, 200, 30))
            surf.blit(highlight, (self.truepos[0], self.truepos[1]))

        if self.piece:
            self.piece.draw(surf, self.truepos[0], self.truepos[1])

        if self.marked:
            marker = pygame.Surface((75, 75), pygame.SRCALPHA, 32)
            marker.set_alpha(128)
            pygame.draw.circle(marker, (239, 66, 245), (37, 37), 10)
            surf.blit(marker, (self.truepos[0], self.truepos[1]))


    def set_highlight(self, bool_value):
        self.highlighted = bool_value

    def set_marked(self, bool_value):
        self.marked = bool_value

    def set_piece(self, piece_object):
        self.piece = piece_object

    def get_coords(self):
        return self.coords

    def get_piece_name(self):
        if self.piece:
            return self.piece.get_name()
        else:
            return None


class Piece:
    def __init__(self, name, image):
        self.name = name
        self.image = image.convert_alpha()

    def draw(self, surf, x, y):
        surf.blit(self.image, (x, y))

    def get_name(self):
        return self.name


class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (480, 160))
        self.meta_data = self.filename.replace("png", "json")
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def parse_sprite(self, name):
        sprite = self.data['pieces'][name]["frame"]
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image

    # noinspection PyTypeChecker
    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite
