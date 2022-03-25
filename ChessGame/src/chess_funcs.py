from chess_classes import Piece
from chess_data import directions, knight_directions


def fill_board(board_list, spritesheet):
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


def select_new_square(current, target, board_state):
    if current: current.set_highlight(False)

    current = target
    current.set_highlight(True)
    draggging = current.piece
    potential = get_moves(board_state, current.get_coords(), current.piece.get_name())
    current.set_piece(None)

    return current, draggging, potential


def deselect_square(selected):
    if selected:
        selected.set_highlight(False)
    selected = None
    movelist = []
    return selected, movelist


def move_piece(start_square, end_square):
    end_square.set_piece(start_square.piece)
    start_square.set_piece(None)


# def collision_check(board_list, x, y):
#     pass


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


def get_moves(board_state, origin, piece_type):
    print("==================Getting moves...", piece_type)
    x, y = origin
    response = []
    if piece_type == 'wpawn':
        print("wpawn")
        if y == 6:
            response.append(board_state[x][y-2])
        response.append(board_state[x][y-1])
    elif piece_type[1:] == "bish":
        print("bish")
        response += rec_add_squares(board_state, x, y, "upleft", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "upright", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "downleft", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "downright", piece_type[0], [])
    elif piece_type[1:] == "rook":
        print("rook")
        response += rec_add_squares(board_state, x, y, "up", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "down", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "left", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "right", piece_type[0], [])
    elif piece_type[1:] == "quee":
        print("quee")
        for key in directions:
            response += rec_add_squares(board_state, x, y, key, piece_type[0], [])
    elif piece_type[1:] == "knig":
        print("knig")
        for key in knight_directions:
            xmod, ymod = knight_directions[key]
            tempx = x + xmod
            tempy = y + ymod
            if (tempx < 0) or (tempx > 7) or (tempy < 0) or (tempy > 7):
                pass
            elif board_state[tempx][tempy].piece:
                print("Piece")
                if board_state[tempx][tempy].piece.get_name()[0] != piece_type[0]:
                    print("enemy!")
                    response.append(board_state[tempx][tempy])
            else:
                response.append(board_state[tempx][tempy])
    for e in response: print(e)
    return response
