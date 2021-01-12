# from Quiz import data_to_quiz
from clients.Player import Player


class Room():
    def __init__(self, host, pin):
        self.host = host
        self.pin = pin
        self.players = []
        self.quiz = None

    def get_players_ranking(self):
        caculate_score_of_player(self)
        result = []
        players = sorted(self.players, key=lambda x: x.score, reverse=True)
        for player in players:
            rank = players.index(player) + 1 
            player.ranking = rank 
            result.append({"nickname":player.nickname,"score":player.score, "rank":rank})
        return result

    def find_player_in_room(self, nick_name:str) -> Player:
        for player in self.players:
            if player.nickname == nick_name:
                return player
        return None

def caculate_score_of_player(self):
    print(self)
    for player in self.players:
        player.score = 0
        streak = 0
        for i in range(len(player.answers)):
            if player.answers[i] == self.quiz.rights[i]:
                streak += 1
                player.score = player.score + 100 + 50*streak
            else:
                streak
       

 
# room = Room(12,15)
# quiz = data_to_quiz("data.json")
# room.quiz = quiz[-1]  
# print(quiz[-1].rights)
# player1 = Player("p1",room)
# player1.answers = [1,1]
# # player1.score = 100
# player2 = Player("p2",room)
# player2.answers = [0,1]

# # player2.score = 2000
# player3 = Player("p3",room)
# player3.answers = [1,0]
# # player3.score = 300
# room.players.append(player1)
# room.players.append(player2)
# room.players.append(player3)
# result2 = room.get_players_ranking()

# print(result2)



# room.players.append(9)
# room.players.append(945)
# room.players.append(9452)
# print(room.players)

