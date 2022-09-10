import pygame
from chess_classes import Spritesheet, Square, Piece
from chess_data import bg_colour
from chess_funcs import (
    fill_board, select_new_square, deselect_square, handle_moving, render_scoreboard
)
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


# //////////////////////// Setup //////////////////////////////////////////////////////////////
# Initialise pygame.
class ChessGame(ConnectionListener):
    def __init__(self, host, port):
        pygame.init()
        self.win = pygame.display.set_mode((830, 620))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.gameid = None
        self.num = None

        self.spritesheet = Spritesheet('Sprites/sprite_sheet.png')

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
        self.white_to_play = True
        self.potential_squares = []
        self.taken_pieces = [
            [[]],
            [[]]
        ]
        self.dragging_piece = None
        self.mousedown = False

        self.Connect((host, port))

        self.running = False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)

        if self.num == 0:
            self.turn = True
            self.playingWhite = True
        else:
            self.turn = False
            self.playingWhite = False


    @staticmethod
    def Network_disconnected(data):
        print("======================================")
        print("The game server appears to be offline.")
        print("             Closing game.            ")
        print("======================================")
        quit()

    def Network_startgame(self, data):
        print("Multiplayer game has started!")
        self.running = True
        self.num = data["player"]
        self.gameid = data["gameid"]


    def Network_boardupdate(self, data):  # TODO
        print("Detected move data")
        self.turn = True
        self.white_to_play = not self.white_to_play
        
        start_coords = data["start_coords"]
        end_coords = data["end_coords"]
        start_piece = data["start_piece"]
        end_piece = data["end_piece"]
        event = data["event"]

        self.board[end_coords[0]][end_coords[1]].set_piece(Piece(end_piece,
                                                                 self.spritesheet.parse_sprite(end_piece)))


        if start_piece:
            if event == "take":
                taken_piece = Piece(start_piece, self.spritesheet.parse_sprite(start_piece))
                if start_piece[0] == "w":
                    if start_piece[1:] == "pawn":
                        self.taken_pieces[0][0].append(taken_piece)
                    else:
                        self.taken_pieces[0].append(taken_piece)
                else:
                    if start_piece[1:] == "pawn":
                        self.taken_pieces[1][0].append(taken_piece)
                    else:
                        self.taken_pieces[1].append(taken_piece)
                self.board[start_coords[0]][start_coords[1]].set_piece(None)
        else:
            self.board[start_coords[0]][start_coords[1]].set_piece(None)


    def draw_board(self):
        # ==================== GRAPHICS DRAWING ====================
        mouse = pygame.mouse.get_pos()
        self.win.fill(bg_colour)
        render_scoreboard(self.win, self.taken_pieces, self.white_to_play, self.playingWhite, self.turn)
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
        if (10 < mouse[0] < 610) and (10 < mouse[1] < 610) and self.turn:  # If mouse on the board...
            click = pygame.mouse.get_pressed(3)[0]  # Get state of Mouse1
            target_square = self.board[int((mouse[0] - 10) / 75)][int((mouse[1] - 10) / 75)]

            if not click:  # If mouse1 is up
                if self.mousedown and self.selected_square:  # If unclicking
                    self.selected_square.set_piece(self.dragging_piece)
                    if target_square in self.potential_squares:  # If dropping onto a potential move
                        self.potential_squares, event = handle_moving(
                            self.selected_square, target_square, self.spritesheet,
                            self.win, self.clock, self.taken_pieces
                        )
                        print("Resolved==============\n",
                              self.selected_square, "\n",
                              target_square)
                        self.Send({"action": "move",
                                   "num": self.num,
                                   "gameid": self.gameid,
                                   "event": event,
                                   "start_coords": self.selected_square.get_coords(),
                                   "end_coords": target_square.get_coords(),
                                   "start_piece": self.selected_square.get_piece_name(),
                                   "end_piece": target_square.get_piece_name()})
                        self.white_to_play = not self.white_to_play
                        self.turn = False
                        if (event == "take") or (event == "move"):
                            self.selected_square.set_piece(None)
                        self.selected_square = None
                    self.dragging_piece = None
                self.mousedown = False

            elif click and (not self.mousedown):  # If clicking down
                self.mousedown = True
                if target_square in self.potential_squares:  # If clicking on a potential move
                    self.potential_squares, event = handle_moving(
                        self.selected_square, target_square, self.spritesheet,
                        self.win, self.clock, self.taken_pieces
                    )
                    print("Resolved==============\n",
                          self.selected_square, "\n",
                          target_square)
                    self.Send({"action": "move",
                               "num": self.num,
                               "gameid": self.gameid,
                               "event": event,
                               "start_coords": self.selected_square.get_coords(),
                               "end_coords": target_square.get_coords(),
                               "start_piece": self.selected_square.get_piece_name(),
                               "end_piece": target_square.get_piece_name()})
                    self.white_to_play = not self.white_to_play
                    self.turn = False
                    if (event == "take") or (event == "move"):
                        self.selected_square.set_piece(None)
                    self.selected_square = None
                elif target_square.piece:  # Otherwise, if selecting a new piece
                    self.selected_square, self.dragging_piece, self.potential_squares = select_new_square(
                        self.white_to_play, self.selected_square, target_square, board_state=self.board
                    )
                else:  # Else, if selecting a blank, unreachable square
                    self.selected_square, self.potential_squares = deselect_square(self.selected_square)

        # Draw and update
        self.draw_board()
        pygame.display.flip()


    @staticmethod
    def Network(data):
        print("~~~Incoming data- ", data)


game = ChessGame('localhost', 8001)
while True:
    game.update()
