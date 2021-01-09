
import json
from module.Room import Room


class Host():
    def __init__(self, username, password, session="none", addr="none", current_room : Room = None, current_quiz="none"):
        self.username = username
        self.password = password
        self.session = session
        self.addr = addr
        self.current_room = current_room
        self.current_quiz = current_quiz

def check_usr_valid(usr:str)-> bool:
    file = open("user.json")
    users = json.load(file)
    for user in users:
        username = user['username']
        if(usr == username ):
            return False
    return True

def check_host_exsist(usr:str, passwd:str)-> bool:
    file = open("user.json")
    users = json.load(file)
    for user in users:
        username = user['username']
        password = user['password']
        if(usr == username and passwd == password):
            return True
    return False

def append_user(usr:str, passwd:str):
    with open('user.json') as f:
        data = json.load(f)

    data.append({"username":usr,"password":passwd})

    with open('user.json', 'w') as f:
        json.dump(data, f)
# result = check_usr_valid("sddssd")
# print(result)
# result = check_host_exsist("admin2","admin2")
# print(result)
# room = Room(12,15)
# room.players.append(9)
# room.players.append(945)
# room.players.append(9452)
# print(room.players)

