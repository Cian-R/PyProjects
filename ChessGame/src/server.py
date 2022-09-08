import PodSixNet
from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server


class ClientChannel(Channel):
    def Network(self, data):
        print(f"DATA: {data}")

    def Network_place(self, data):
        # deconsolidate all of the data from the dictionary

        # horizontal or vertical?
        hv = data["is_horizontal"]
        # x of placed line
        x = data["x"]

        # y of placed line
        y = data["y"]

        # player number (1 or 0)
        num = data["num"]

        # id of game given by server at start of game
        self.gameid = data["gameid"]

        # tells server to place line
        self._server.placeLine(hv, x, y, data, self.gameid, num)


class ChessServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
        print("Initialised.")

    def makeMove(self, is_h, x, y, data, gameid, num):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].placeLine(is_h, x, y, data, num)

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
        # whose turn
        self.turn = 0
        # owner map
        self.owner = [[False for x in range(6)] for y in range(6)]
        # Seven lines in each direction to make a six by six grid.
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        # initialize the players including the one who started the game
        self.player0 = player0
        self.player1 = None
        # gameid of game
        self.gameid = current_index

    def makeMove(self, is_h, x, y, data, num):  # TODO
        # make sure it's their turn
        if num == self.turn:
            self.turn = 0 if self.turn else 1
            # place line in game
            if is_h:
                self.boardh[y][x] = True
            else:
                self.boardv[y][x] = True
            # send data and turn data to each player
            self.player0.Send(data)
            self.player1.Send(data)



print("STARTING SERVER ON LOCALHOST")
chess_server = ChessServer(localaddr=('localhost', 8001))
while True:
    chess_server.Pump()
    sleep(0.01)

