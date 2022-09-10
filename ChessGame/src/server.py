import PodSixNet
from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server


class ClientChannel(Channel):
    def Network(self, data):
        print(f"DATA: {data}")

    def Network_move(self, data):
        print("Move made?")
        # Grab data

        num = data["num"]
        board = data["board"]
        gameid = data["gameid"]

        self._server.updateBoard(board, gameid, num)


class ChessServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
        print("Server Initialised.")

    def updateBoard(self, board, gameid, num):
        print("Update a board")
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].updateBoard(board, num)

    def Connected(self, channel, addr):
        print('new connection:', str(channel), str(addr))
        if self.queue is None:
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
        else:
            channel.gameid = self.currentIndex
            self.queue.player1 = channel
            self.queue.player0.Send({"action": "startgame", "player": 0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame", "player": 1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue = None


class Game:
    def __init__(self, player0, current_index):
        print("Game initialised")
        # Initialize the players, gameid and turn
        self.player0 = player0
        self.player1 = None
        self.gameid = current_index
        self.turn = 0

        # Game State Variables
        self.board_state = None

    def updateBoard(self, board, num):
        print("Game update board")
        # Make sure it's their turn
        if num == self.turn:
            self.turn = 0 if self.turn else 1

            self.board_state = board

            self.player0.Send({"action": "boardupdate", "board": self.board_state})
            self.player1.Send({"action": "boardupdate", "board": self.board_state})



print("STARTING SERVER ON LOCALHOST")
chess_server = ChessServer(localaddr=('localhost', 8001))
while True:
    chess_server.Pump()
    sleep(0.01)

