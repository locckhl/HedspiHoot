
class Player():
    def __init__(self, nickname, current_room):
        self.nickname = nickname
        self.current_room = current_room
        self.ranking = 0
        self.score = 0
        self.answers = []

    def get_result(self):
        return f'Score: {self.score};Ranking: {self.ranking}'
   
# room = Room(12,15)
# room.players.append(9)
# room.players.append(945)
# room.players.append(9452)
# print(room.players)

