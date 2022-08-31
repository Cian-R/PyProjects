import PodSixNet
from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server


class ClientChannel(Channel):
    def Network(self, data):
        print(f"DATA: {data}")


class MyServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        print("Initialised.")

    def connected(self, channel, addr):
        print(f"new connection: {channel}")


print("STARTING SERVER ON LOCALHOST")
myserver = MyServer(localaddr=('localhost', 1337))
while True:
    myserver.Pump()
    sleep(0.01)

