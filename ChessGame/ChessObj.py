import pygame
from chess_classes import Spritesheet, Square, Piece
from chess_data import bg_colour


def fill_board(board_list):
    for indx, valx in enumerate(board_list):
        for indy, valy in enumerate(valx):
            if indy == 1:
                board_list[indx][indy].set_piece(Piece('bpawn', spritesheet.parse_sprite('bpawn')))
            if indy == 6:
                board_list[indx][indy].set_piece(Piece('wpawn', spritesheet.parse_sprite('wpawn')))

    board_list[0][0].set_piece(Piece('brook', spritesheet.parse_sprite('brook')))
    board_list[1][0].set_piece(Piece('bknig', spritesheet.parse_sprite('bknig')))
    board_list[2][0].set_piece(Piece('bbish', spritesheet.parse_sprite('bbish')))
    board_list[3][0].set_piece(Piece('bquee', spritesheet.parse_sprite('bquee')))
    board_list[4][0].set_piece(Piece('bking', spritesheet.parse_sprite('bking')))
    board_list[5][0].set_piece(Piece('bbish', spritesheet.parse_sprite('bbish')))
    board_list[6][0].set_piece(Piece('bknig', spritesheet.parse_sprite('bknig')))
    board_list[7][0].set_piece(Piece('brook', spritesheet.parse_sprite('brook')))

    board_list[0][7].set_piece(Piece('wrook', spritesheet.parse_sprite('wrook')))
    board_list[1][7].set_piece(Piece('wknig', spritesheet.parse_sprite('wknig')))
    board_list[2][7].set_piece(Piece('wbish', spritesheet.parse_sprite('wbish')))
    board_list[3][7].set_piece(Piece('wquee', spritesheet.parse_sprite('wquee')))
    board_list[4][7].set_piece(Piece('wking', spritesheet.parse_sprite('wking')))
    board_list[5][7].set_piece(Piece('wbish', spritesheet.parse_sprite('wbish')))
    board_list[6][7].set_piece(Piece('wknig', spritesheet.parse_sprite('wknig')))
    board_list[7][7].set_piece(Piece('wrook', spritesheet.parse_sprite('wrook')))

    return board_list


pygame.init()

win = pygame.display.set_mode((620, 620))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()

# /////////////////////////////////////////////////////// Setup //////////////////////////////////////////////////////
board = []
spritesheet = Spritesheet("Sprites/sprite_sheet.png")

# Initiate squares
for board_x in range(8):
    row = []
    for board_y in range(8):
        new_square = Square((board_x + board_y) % 2 == 0, [board_x, board_y])
        row.append(new_square)
    board.append(row)

board = fill_board(board)

# /////////////////////////////////////////////////////// Main ///////////////////////////////////////////////////////
selected_square = None
dragging_piece = None
mousedown = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # =========================================================
    mouse = pygame.mouse.get_pos()
    if (10 < mouse[0] < 610) and (10 < mouse[1] < 610):  # If mouse within the board boundary...
        click = pygame.mouse.get_pressed()
        target_square = board[int((mouse[0] - 10) / 75)][int((mouse[1] - 10) / 75)]

        if not click[0]:  # If mouse1 is up
            if mousedown and selected_square:  # If unclicking...
                selected_square.set_piece(dragging_piece)
                dragging_piece = None
            mousedown = False

        if click[0] and (not mousedown):  # If mouse1 is clicked down
            mousedown = True
            if target_square.piece:
                if selected_square: selected_square.highlighted = False
                selected_square = target_square
                selected_square.highlighted = True
                dragging_piece = selected_square.piece
                selected_square.set_piece(None)
            else:
                if selected_square: selected_square.highlighted = False
                selected_square = None

    # ==================== GRAPHICS DRAWING ====================
    win.fill(bg_colour)
    for row in board:
        for square in row:
            square.draw(win)
    if dragging_piece:
        dragging_piece.draw(win, mouse[0]-35, mouse[1]-37)
    # =========================================================

    pygame.display.update()
    clock.tick(30)
