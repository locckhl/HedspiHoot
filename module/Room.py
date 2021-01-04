
from module.State import State


class Room():
    def __init__(self, host, pin):
        self.host = host
        self.pin = pin
        self.players = []
        self.state = State.LOBBY
        self.quiz = None

   
room = Room(12,15)
room.players.append(9)
room.players.append(945)
room.players.append(9452)
print(room.players)

