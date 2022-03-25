from chess_classes import Piece, Square
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


def select_new_square(current: Square, target: Square, board_state):
    if current: current.set_highlight(False)

    current = target
    current.set_highlight(True)
    draggging = current.piece
    potential = get_moves(board_state, current.get_coords(), current.piece.get_name())
    current.set_piece(None)

    return current, draggging, potential


def deselect_square(current: Square):
    if current:
        current.set_highlight(False)
    current = None
    movelist = []
    return current, movelist


def handle_moving(current: Square, target: Square, spritesheet):
    if target.piece:  # If there's an enemy piece
        pass
    move_piece(current, target)
    if target.piece.get_name()[1:] == "pawn":
        if target.get_coords()[1] == 0:
            promote_pawn(target, "w", spritesheet)
        elif target.get_coords()[1] == 7:
            promote_pawn(target, "b", spritesheet)
    selected_square, potential_squares = deselect_square(current)
    return selected_square, potential_squares


def move_piece(start_square: Square, end_square: Square):
    end_square.set_piece(start_square.piece)
    start_square.set_piece(None)


def promote_pawn(pawn_square: Square, colour, spritesheet):
    #  Probably render some sort fo selection box here :/
    pawn_square.set_piece(Piece(f'{colour}quee', spritesheet.parse_sprite(f'{colour}quee')))


def rec_add_squares(board_state, x, y, direction, colour, collected: list):
    xmod, ymod = directions[direction]
    x += xmod
    y += ymod
    if (x < 0) or (x > 7) or (y < 0) or (y > 7):
        return collected
    elif board_state[x][y].piece:
        if board_state[x][y].piece.get_name()[0] != colour:
            collected.append(board_state[x][y])
        return collected
    else:
        collected.append(board_state[x][y])
        collected = rec_add_squares(board_state, x, y, direction, colour, collected)
        return collected


def get_moves(board_state, origin, piece_type):
    x, y = origin
    response = []
    if piece_type == 'wpawn':
        if not board_state[x][y - 1].piece:
            response.append(board_state[x][y - 1])
            if (y == 6) and (not board_state[x][y - 2].piece):
                response.append(board_state[x][y - 2])

    elif piece_type == 'bpawn':
        if not board_state[x][y + 1].piece:
            response.append(board_state[x][y + 1])
            if (y == 1) and (not board_state[x][y + 2].piece):
                response.append(board_state[x][y + 2])

    elif piece_type[1:] == "bish":
        response += rec_add_squares(board_state, x, y, "upleft", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "upright", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "downleft", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "downright", piece_type[0], [])

    elif piece_type[1:] == "rook":
        response += rec_add_squares(board_state, x, y, "up", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "down", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "left", piece_type[0], [])
        response += rec_add_squares(board_state, x, y, "right", piece_type[0], [])

    elif piece_type[1:] == "quee":
        for key in directions:
            response += rec_add_squares(board_state, x, y, key, piece_type[0], [])

    elif piece_type[1:] == "king":
        for key in directions:
            xmod, ymod = directions[key]
            tempx = x + xmod
            tempy = y + ymod
            if (tempx < 0) or (tempx > 7) or (tempy < 0) or (tempy > 7):
                pass
            elif board_state[tempx][tempy].piece:
                if board_state[tempx][tempy].piece.get_name()[0] != piece_type[0]:
                    response.append(board_state[tempx][tempy])
            else:
                response.append(board_state[tempx][tempy])

    elif piece_type[1:] == "knig":
        for key in knight_directions:
            xmod, ymod = knight_directions[key]
            tempx = x + xmod
            tempy = y + ymod
            if (tempx < 0) or (tempx > 7) or (tempy < 0) or (tempy > 7):
                pass
            elif board_state[tempx][tempy].piece:
                if board_state[tempx][tempy].piece.get_name()[0] != piece_type[0]:
                    response.append(board_state[tempx][tempy])
            else:
                response.append(board_state[tempx][tempy])

    return response
