import pygame
import json

whiteSq = (238, 238, 210)
blackSq = (118, 150, 86)


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

    def __str__(self):
        if self.piece:
            return f"<<Square - {self.piece.name}>> {str(self.piece)} {str(self.coords)}"
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

    def set_piece(self, piece_object):
        self.piece = piece_object


class Piece:
    def __init__(self, name, image):
        self.name = name
        self.image = image.convert_alpha()
        self.movelist = None  # TODO: Uhh, maybe using a json file?

    def draw(self, surf, x, y):
        surf.blit(self.image, (x, y))


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

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA, 32)  # Honestly not sure why this works, but it does.
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite
