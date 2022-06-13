import pygame

pygame.init()
win = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Isometric Tests')
clock = pygame.time.Clock()

# /////////////////////////////////////////////////////// ----- //////////////////////////////////////////////////////
sprite = "isoimg.png"
isocube = pygame.image.load(sprite).convert()
isocube = pygame.transform.scale(isocube, (100, 100))
isocube.set_colorkey((255, 255, 255))

x_offset = 500
y_offset = 200
x1 = int(input("X: "))
y1 = int(input("Y: "))
x2 = int(input("X: "))
y2 = int(input("Y: "))
x3 = int(input("X: "))
y3 = int(input("Y: "))


def generate_iso_field(length, breadth, layer):
    board = []
    w = min(length, breadth)
    r = length + breadth - 1
    startrow = r - w + 1
    for rowno in range(1, r + 1):
        for b in range(min(rowno, w) - max(0, rowno - startrow)):
            board.append(
                [
                    x_offset - (rowno * 50) + (b * 100) + (max(rowno - length, 0) * 100),  # X-Coord of the Cube
                    y_offset + (rowno * 25) - (layer * 50)  # Y-Coord of the Cube
                ]
            )
    return board


gameboard = [generate_iso_field(x1, y1, 0), generate_iso_field(x2, y2, 1), generate_iso_field(x3, y3, 2)]

print(gameboard)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    win.fill((100, 200, 200))
    for layer in gameboard:
        for coord in layer:
            win.blit(isocube, (coord[0], coord[1]))

    pygame.display.flip()
