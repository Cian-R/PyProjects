import pygame
from chess_classes import Spritesheet, Square
from chess_data import bg_colour
from chess_funcs import (
    fill_board, select_new_square, deselect_square, handle_moving
)

# //////////////////////// Setup //////////////////////////////////////////////////////////////
# Initialise pygame.
pygame.init()
win = pygame.display.set_mode((620, 620))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()

spritesheet = Spritesheet("src/Sprites/sprite_sheet.png")

# Initiate squares and fill board
board = []
for board_x in range(8):
    row = []
    for board_y in range(8):
        new_square = Square((board_x + board_y) % 2 == 0, [board_x, board_y])
        row.append(new_square)
    board.append(row)

board = fill_board(board, spritesheet)

# //////////////////////// Main ///////////////////////////////////////////////////////////////
# Initialise values
selected_square = None
potential_squares = []
dragging_piece = None
mousedown = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    # =========================================================================================
    mouse = pygame.mouse.get_pos()
    if (10 < mouse[0] < 610) and (10 < mouse[1] < 610):  # If mouse on the board...
        click = pygame.mouse.get_pressed(3)[0]  # Get state of Mouse1
        target_square = board[int((mouse[0] - 10) / 75)][int((mouse[1] - 10) / 75)]

        if not click:  # If mouse1 is up
            if mousedown and selected_square:  # If unclicking
                selected_square.set_piece(dragging_piece)
                if target_square in potential_squares:  # If dropping onto a potential move
                    selected_square, potential_squares = handle_moving(
                        selected_square, target_square, spritesheet
                    )
                dragging_piece = None
            mousedown = False

        if click and (not mousedown):  # If clicking down
            mousedown = True
            if target_square in potential_squares:  # If clicking on a potential move
                selected_square, potential_squares = handle_moving(
                    selected_square, target_square, spritesheet
                )
            elif target_square.piece:   # Otherwise, if selecting a new piece
                selected_square, dragging_piece, potential_squares = select_new_square(
                    selected_square, target_square, board_state=board
                )
            else:   # Else, if selecting a blank, unreachable square
                selected_square, potential_squares = deselect_square(selected_square)

    # ==================== GRAPHICS DRAWING ====================
    win.fill(bg_colour)
    for row in board:
        for squareObj in row:
            squareObj.set_marked(False)
            if squareObj in potential_squares:
                squareObj.set_marked(True)
            squareObj.draw(win)
    if dragging_piece:
        dragging_piece.draw(win, mouse[0]-35, mouse[1]-37)
    # =========================================================
    pygame.display.update()
    clock.tick(60)
