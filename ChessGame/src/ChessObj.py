import pygame
from chess_classes import Spritesheet, Square
from chess_data import bg_colour
from chess_funcs import (
    fill_board, select_new_square, deselect_square, handle_moving
)
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


# //////////////////////// Setup //////////////////////////////////////////////////////////////
# Initialise pygame.
class ChessGame(ConnectionListener):
    def __init__(self, host, port):
        pygame.init()
        self.win = pygame.display.set_mode((620, 620))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()

        self.spritesheet = Spritesheet("Sprites/sprite_sheet.png")

        # Initiate squares and fill board
        self.board = []
        for board_x in range(8):
            board_row = []
            for board_y in range(8):
                new_square = Square((board_x + board_y) % 2 == 0, [board_x, board_y])
                board_row.append(new_square)
            self.board.append(board_row)

        self.board = fill_board(self.board, self.spritesheet)

        self.selected_square = None
        self.potential_squares = []
        self.dragging_piece = None
        self.mousedown = False

        self.Connect((host, port))

    def draw_board(self):
        # ==================== GRAPHICS DRAWING ====================
        mouse = pygame.mouse.get_pos()
        self.win.fill(bg_colour)
        for row in self.board:
            for squareObj in row:
                squareObj.set_marked(False)
                if squareObj in self.potential_squares:
                    squareObj.set_marked(True)
                squareObj.draw(self.win)
        if self.dragging_piece:
            self.dragging_piece.draw(self.win, mouse[0] - 35, mouse[1] - 37)
        # =========================================================

    def update(self):
        self.clock.tick(60)
        connection.Pump()
        self.Pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        mouse = pygame.mouse.get_pos()
        if (10 < mouse[0] < 610) and (10 < mouse[1] < 610):  # If mouse on the board...
            click = pygame.mouse.get_pressed(3)[0]  # Get state of Mouse1
            target_square = self.board[int((mouse[0] - 10) / 75)][int((mouse[1] - 10) / 75)]

            if not click:  # If mouse1 is up
                if self.mousedown and self.selected_square:  # If unclicking
                    self.selected_square.set_piece(self.dragging_piece)
                    if target_square in self.potential_squares:  # If dropping onto a potential move
                        self.selected_square, self.potential_squares = handle_moving(
                            self.selected_square, target_square, self.spritesheet, self.win, self.clock
                        )
                    self.dragging_piece = None
                self.mousedown = False

            if click and (not self.mousedown):  # If clicking down
                self.mousedown = True
                if target_square in self.potential_squares:  # If clicking on a potential move
                    self.selected_square, self.potential_squares = handle_moving(
                        self.selected_square, target_square, self.spritesheet, self.win, self.clock
                    )
                elif target_square.piece:  # Otherwise, if selecting a new piece
                    self.selected_square, self.dragging_piece, self.potential_squares = select_new_square(
                        self.selected_square, target_square, board_state=self.board
                    )
                else:  # Else, if selecting a blank, unreachable square
                    self.selected_square, self.potential_squares = deselect_square(self.selected_square)

        # Draw and update
        self.draw_board()
        pygame.display.flip()

    @staticmethod
    def Network(data):
        print(data)


game = ChessGame('localhost', 1337)
while True:
    game.update()
