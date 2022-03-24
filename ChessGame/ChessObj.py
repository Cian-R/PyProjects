import pygame
from chess_classes import Spritesheet, Square, Piece
from chess_data import bg_colour, directions, knight_directions


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

    board_list[2][4].set_piece(Piece('wrook', spritesheet.parse_sprite('wrook')))
    board_list[4][4].set_piece(Piece('wquee', spritesheet.parse_sprite('wquee')))
    board_list[4][3].set_piece(Piece('wknig', spritesheet.parse_sprite('wknig')))
    board_list[6][4].set_piece(Piece('wbish', spritesheet.parse_sprite('wbish')))

    return board_list


def collision_check(board_list, x, y):
    pass


def rec_add_squares(board_state, x, y, direction, colour, collected):
    print("Recursion Start:", x, y, direction, colour, collected)
    xmod, ymod = directions[direction]
    print(xmod, ymod)
    x += xmod
    y += ymod
    print(x, y)
    if (x < 0) or (x > 7) or (y < 0) or (y > 7):
        print("EDGEEEEE")
        return collected
    elif board_state[x][y].piece:
        print("Piece")
        if board_state[x][y].piece.get_name()[0] != colour:
            print("enemy!")
            collected.append(board_state[x][y])
        return collected
    else:
        print("Recursion End:", x, y, direction)
        collected.append(board_state[x][y])
        collected = rec_add_squares(board_state, x, y, direction, colour, collected)
        return collected


def get_moves(game_board, origin, piece_type):
    print("==================Getting moves...", piece_type)
    x, y = origin
    response = []
    if piece_type == 'wpawn':
        print("wpawn")
        if y == 6:
            response.append(game_board[x][y-2])
        response.append(game_board[x][y-1])
    elif piece_type[1:] == "bish":
        print("bish")
        response += rec_add_squares(game_board, x, y, "upleft", piece_type[0], [])
        response += rec_add_squares(game_board, x, y, "upright", piece_type[0], [])
        response += rec_add_squares(game_board, x, y, "downleft", piece_type[0], [])
        response += rec_add_squares(game_board, x, y, "downright", piece_type[0], [])
    elif piece_type[1:] == "rook":
        print("rook")
        response += rec_add_squares(game_board, x, y, "up", piece_type[0], [])
        response += rec_add_squares(game_board, x, y, "down", piece_type[0], [])
        response += rec_add_squares(game_board, x, y, "left", piece_type[0], [])
        response += rec_add_squares(game_board, x, y, "right", piece_type[0], [])
    elif piece_type[1:] == "quee":
        print("quee")
        for key in directions:
            response += rec_add_squares(game_board, x, y, key, piece_type[0], [])
    elif piece_type[1:] == "knig":
        print("knig")
        for key in knight_directions:
            xmod, ymod = knight_directions[key]
            tempx = x + xmod
            tempy = y + ymod
            if (tempx < 0) or (tempx > 7) or (tempy < 0) or (tempy > 7):
                pass
            elif game_board[tempx][tempy].piece:
                print("Piece")
                if game_board[tempx][tempy].piece.get_name()[0] != piece_type[0]:
                    print("enemy!")
                    response.append(game_board[tempx][tempy])
            else:
                response.append(game_board[tempx][tempy])
    for e in response: print(e)
    return response


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
potential_squares = []
dragging_piece = None
mousedown = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # =========================================================
    mouse = pygame.mouse.get_pos()
    if (10 < mouse[0] < 610) and (10 < mouse[1] < 610):  # If mouse on the board...
        click = pygame.mouse.get_pressed(3)[0]  # Get state of Mouse1
        target_square = board[int((mouse[0] - 10) / 75)][int((mouse[1] - 10) / 75)]

        if not click:  # If mouse1 is up
            if mousedown and selected_square:  # If unclicking...
                selected_square.set_piece(dragging_piece)
                dragging_piece = None
            mousedown = False

        if click and (not mousedown):  # If mouse1 is clicked down
            mousedown = True
            if target_square.piece:
                if selected_square: selected_square.set_highlight(False)
                selected_square = target_square
                selected_square.set_highlight(True)
                dragging_piece = selected_square.piece
                potential_squares = get_moves(board, selected_square.get_coords(),
                                              selected_square.piece.get_name())
                selected_square.set_piece(None)
            else:
                if selected_square: selected_square.set_highlight(False)
                selected_square = None
                potential_squares = []

            print(potential_squares)

    # =========================================================


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
