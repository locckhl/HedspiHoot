from clients.Host import Host, append_user, check_host_exsist, check_usr_valid
import json
from module.MessType import MessType
from module.Messages import Messages, convert_message
from module.Quiz import data_to_quiz, find_quiz_by_user, quiz_package_handle
from clients.Player import Player
from module.Room import Room
from module.State import *
import threading
import socket
import time
import sys
import random
import ast
from env import SERVER_IP, TIME
import string
import random

host = SERVER_IP
port = 55555


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(False)
server.bind((host,port))
server.listen()

clients = []
players = []
hosts = []
nicknames = []
rooms = []
pins = []
sessions = []



def check_session(rmessage:Messages)-> bool:
    if rmessage.type == MessType.REQUEST_ROLE.name or rmessage.type == MessType.REQUEST_SIGN_IN.name or rmessage.type == MessType.REQUEST_SIGN_UP.name or rmessage.type == MessType.SET_NICKNAME.name or rmessage.session in sessions:
        return True
    return False

def solveResult(room:Room, host):
    hostResult =room.get_players_ranking()
    host.send(Messages(MessType.HOST_RESULT.name, body=hostResult).to_message())
    # client.send(Messages(MessType.PLAYER_RESULT.name, body=player.get_result()).to_message()) 
    # print(room.players)
    # print(players)
    for player_in_room in room.players:
        for player_dict in players:
            if(player_dict["nickname"] == player_in_room.nickname):
                player_dict["client"].send(Messages(MessType.PLAYER_RESULT.name, body=player_in_room.get_result()).to_message())


def findHost(host_user_name) -> Host:
    # print(host_user_name)
    # print(hosts)
    for host in hosts:
        # print(host.username)
        if(host.username == host_user_name ):
            return host
    return None
def findRoom(room_pin:int) -> Room:
    # print(int)
    for room in rooms:
        # print(room.pin)
        if(room.pin == room_pin ):
            return room
    return None
def broadCast(room:Room, message:Messages):
    # print(room.players)
    # print(players)
    for player_in_room in room.players:
        for player_dict in players:
            if(player_dict["nickname"] == player_in_room.nickname):
                player_dict["client"].send(message.to_message())

    return

def handleClient(client, address):
    while True:
        rmessage = convert_message(client.recv(1024))
        rmessage_type = rmessage.type
        # print(rmessage_type)
        # print(MessType.SEND_ROLE.name)
        # print(rmessage.username)
        if(check_session(rmessage) == False):
            print("Session token failed")
        else:
            if(rmessage_type == MessType.REQUEST_ROLE.name): #1 Client choose role
                if(rmessage.body == "1"):
                    smessage = Messages(MessType.CONFIRM.name, body="You are host")
                elif(rmessage.body == "2"):
                    smessage = Messages(MessType.CONFIRM.name, body="You are client")
                else:
                    smessage = Messages(MessType.CONFIRM.name, state=False , body="Wrong mess")
                client.send(smessage.to_message())
            elif(rmessage_type == MessType.IS_NEW_QUIZ.name): #3 Host quiz 's choice ( new or old ) 
                if(rmessage.body == "1"):
                    client.send(Messages(MessType.CONFIRM.name, body="Input new quiz").to_message())
                    
                else:
                    # file = open("data.json")
                    # data = json.load(file)
                    username = rmessage.username
                    data = find_quiz_by_user(username)
                    # print(f"data:{data}")
                    client.send(Messages(MessType.RESPONSE_QUIZZES.name, body=data).to_message())

                
            elif(rmessage_type == MessType.SEND_NEW_QUIZ.name): #4
                name, noQuest, noAns, questions, answers, rights = rmessage.body.split(';')
                username = rmessage.username
                # print(name, noQuest, noAns, questions, answers, rights)
                quiz_package_handle(name, int(noQuest), int(noAns), ast.literal_eval(questions), ast.literal_eval(answers), ast.literal_eval(rights), username)       
                quizzes = data_to_quiz("data.json")
                current_quiz = quizzes[-1]
                host = findHost(username)
                if(host != None):
                    host.current_quiz = current_quiz

                pin = random.randint(1,20)
                while (pin in pins):
                    pin = random.randint(1,20)
                pins.append(pin)
                client.send(Messages(MessType.SEND_PIN.name, body=pin).to_message())
                room = Room(address, pin)
                rooms.append(room)
                current_room = rooms[-1]

                host = findHost(username)
                if(host != None):
                    host.current_room = current_room
                    host.current_room.quiz = current_quiz
                
            elif(rmessage_type == MessType.SEND_QUIZ_CHOICE.name): #6
                username = rmessage.username
                choice = int(rmessage.body) - 1
                find_quiz_by_user(username)
                quizzes = data_to_quiz("data.json", username)
            
                current_quiz = quizzes[choice]
                host = findHost(username)
                if(host != None):
                    host.current_quiz = current_quiz
                    
                
                client.send(Messages(MessType.CONFIRM.name, body=current_quiz.to_string()).to_message())
                
                
                pin = random.randint(1,20)
                while (pin in pins):
                    pin = random.randint(1,20)
                pins.append(pin)
                client.send(Messages(MessType.SEND_PIN.name, body=pin).to_message())
                room = Room(address, pin)
                rooms.append(room)
                current_room = rooms[-1]
                
                host = findHost(username)
                # print("host find", host)

                if(host != None):
                    host.current_room = current_room
                    host.current_room.quiz = current_quiz
                    # print(f"{host.username}")
                    # print(f"{host.current_room}")
                    # print(f"{current_room}")
            elif(rmessage_type == MessType.REQUEST_START_GAME.name): #9
                username = rmessage.username
                host = findHost(username)
                # print(f"{host.username}")
                # print(f"{host.current_room}")
                request_start_game = "no"
                while(request_start_game != "yes" ):
                    client.send(Messages(MessType.SEND_NO_PLAYER.name, body=str(len(host.current_room.players))).to_message())
                    request_start_game = convert_message(client.recv(1024)).body
                # print(request_start_game)
                client.send(Messages(MessType.RESPONSE_START_GAME.name, body="start game").to_message())
                broadCast(host.current_room, Messages(MessType.RESPONSE_START_GAME.name, body="start game"))
                print("Game started")
                time.sleep(TIME+1)
                # host.current_room.caculate_score_of_player()
                # result = host.current_room.get_players_ranking()
                # client.send(Messages(MessType.HOST_RESULT.name, body=result).to_message())
                solveResult(host.current_room, client)

            elif(rmessage_type == MessType.REQUEST_NEXT_QUESTION.name): #12
                username = rmessage.username
                # username = rmessage.username
                host = findHost(username)
                client.send(Messages(MessType.RESPONSE_NEXT_QUESTION.name, body="Next question").to_message())
                # convert_message(client.recv(1024))
                broadCast(host.current_room, Messages(MessType.RESPONSE_NEXT_QUESTION.name, body="Next question"))
                time.sleep(TIME+1)
                # result = host.current_room.get_players_ranking()
                # client.send(Messages(MessType.HOST_RESULT.name, body=result).to_message())
                solveResult(host.current_room, client)


            elif(rmessage_type == MessType.SET_NICKNAME.name): #13
                
                nickname = rmessage.body
                while(nickname in nicknames):
                    client.send(Messages(MessType.IS_VALID_NICKNAME.name, state=False, body="false").to_message())
                    nickname = convert_message(client.recv(1024))

                nicknames.append(nickname)
                print(f"current players: {nicknames}")
                session = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                sessions.append(session)
                client.send(Messages(MessType.IS_VALID_NICKNAME.name, body=session).to_message())

            elif(rmessage_type == MessType.REQUEST_ROOM_PIN.name): #15
                
                room_pin = rmessage.body
                nickname = rmessage.username
                status = "false"
                current_room = None
                for room in rooms:
                    if(int(room_pin) == room.pin):
                        current_room = room
                        status = "true"
                        break
                if status == "true":
                    player = Player(nickname, current_room)
                    players.append({"nickname": nickname, "client": client})
                    current_room.players.append(player)
                    # print(f"Current room: {current_room}")
                    client.send(Messages(MessType.IS_VALID_ROOM_PIN.name, body="true").to_message())

                    # print(f"Current player in room {current_room.pin}")
                    # for player in current_room.players:
                    #     print(f"{player.nickname}")
                else:
                    client.send(Messages(MessType.IS_VALID_ROOM_PIN.name, body="false").to_message())
                    
            elif(rmessage_type == MessType.SEND_ANSWER.name): #19
                nickname = rmessage.username
                pin, answer = rmessage.body.split(';')
                room = findRoom(int(pin))
                if room != None:
                    player = room.find_player_in_room(nickname)
                    player.answers.append(int(answer) - 1)
                   
                else:
                    pass

            elif(rmessage_type == MessType.REQUEST_SIGN_UP.name): #21
                username, password, confirm_password = rmessage.body.split(';')
                if(check_usr_valid(username) and password == confirm_password):
                    host = Host(username,password)
                    hosts.append(host)
                    append_user(username, password)
                    session = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    sessions.append(session)
                    client.send(Messages(MessType.CONFIRM.name, state=True, body=f"sign up successed;{session}").to_message())
                else:
                    client.send(Messages(MessType.CONFIRM.name, state=False, body="sign up falied").to_message())

            elif(rmessage_type == MessType.REQUEST_SIGN_IN.name): #21
                username, password = rmessage.body.split(';')
                if(check_host_exsist(username, password)):
                    host = Host(username,password)
                    hosts.append(host)
                    session = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    sessions.append(session)
                    client.send(Messages(MessType.CONFIRM.name, state=True, body=f"sign in successed;{session}").to_message())
                else:
                    client.send(Messages(MessType.CONFIRM.name, state=False, body="sign in falied").to_message())

            elif(rmessage_type == MessType.END_GAME.name): #23
                username = rmessage.username
                host = findHost(username)
                broadCast(host.current_room, Messages(MessType.END_GAME.name, body="End"))
            elif(rmessage_type == MessType.CLOSE.name): #23
                print(f"Client with address:{str(address)} has been disconnected")
                client.close()
                return
            else:
                pass
    
def main():
    try:
        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            thread = threading.Thread(target=handleClient, args=(client, address, ), daemon=True)
            thread.start()
          
            # print(indirect(int(message.username)))

            

            # if(role == "1"): #Host

            #     thread = threading.Thread(target=handleHost, args=(client, address, ), daemon=True)
            #     thread.start()
            # else: #Player

            #     thread = threading.Thread(target=handlePlayer, args=(client, address, ), daemon=True)
            #     thread.start()

            # while thread.is_alive():
            #     thread.join(1)
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
        server.close()
        sys.exit(1)
        

print("Server is listening...")
if __name__ == "__main__":
    main()
