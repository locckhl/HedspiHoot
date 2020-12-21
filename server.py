import json
from module.Quiz import data_to_quiz, quiz_package_handle
from clients.Player import Player
from module.Room import Room
from module.State import *
import threading
import socket
import time
import sys
import random
import ast
from env import SERVER_IP, SERVER_IP

host = SERVER_IP
port = 55555
TIME = 5

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host,port))
server.listen()

clients = []
nicknames = []
rooms = []
 
def broadcast(message):
    for client in clients:
        client.send(message)

def handleHost(client, address):
    try:
        client.send("You are host".encode("ascii"))
        client.recv(1024).decode("ascii") # nop

        pin = random.randint(1,20)
        client.send(str(pin).encode("ascii"))
        room = Room(address, pin)
        rooms.append(room)
        current_room = rooms[-1]

        choice = str(client.recv(1024).decode("ascii"))

        if(choice == '1'):
            client.send("nop".encode("ascii")) # nop
            name, noQuest, noAns, questions, answers, rights = client.recv(1024).decode("ascii").split(';')
            print(name, noQuest, noAns, questions, answers, rights)
            quiz_package_handle(name, int(noQuest), int(noAns), ast.literal_eval(questions), ast.literal_eval(answers), ast.literal_eval(rights))       
            quizzes = data_to_quiz("data.json")
            current_quiz = quizzes[-1]
        else:
            file = open("data.json")
            data = json.load(file)
            print(f"data:{data}")
            client.send(str(data).encode("ascii"))
            choice = int(client.recv(1024).decode("ascii")) - 1
            quizzes = data_to_quiz("data.json")
           
            current_quiz = quizzes[choice]
            client.send(current_quiz.to_string().encode("ascii"))
            client.recv(1024).decode("ascii") 


        print(f"Current quiz:{current_quiz.name}") 
        room.quiz = current_quiz

        #Lobby
        client.send(str(len(room.players)).encode("ascii"))

        print(f"current_room.state{current_room.state}")
        print(current_room.pin)


        request_start_game = client.recv(1024).decode("ascii")
        while(request_start_game != "y" ):
            client.send(str(len(room.players)).encode("ascii"))
            request_start_game = client.recv(1024).decode("ascii")
        print(request_start_game)
        
        # print(f"player in room {room.pin}:{len(room.players)}")
        
        current_room.state = State.START_GAME
        print(f"current_room.state  {current_room.state}")
        print(current_room.pin)
        # Game started

        # --------------------------------Game started---------------------------------

        for x in range(0,current_room.quiz.noQuest):
            print(x)
            client.send("Show question".encode("ascii"))
            # client.send(current_room.pin).encode("ascii") # Show question
            current_room.state = State.SHOW_QUESTION 
            time.sleep(TIME+1)
            client.send("Result".encode("ascii"))
            current_room.state = State.SHOW_RESULT
            client.recv(1024).decode("ascii") # Continue game
            current_room.state = State.NEXT_QUEST

        client.send("END".encode("ascii")) # Show question

        print("End game")

        client.close()
    except:
        clients.remove(client)
        client.close()


def handlePlayer(client, address):
    try:
        client.send("You are client".encode("ascii"))

        nickname = client.recv(1024).decode("ascii")
        while(nickname in nicknames):
            client.send("false".encode("ascii"))
            nickname = client.recv(1024).decode("ascii")
        client.send("true".encode("ascii"))

        nicknames.append(nickname)
        print(f"current players: {nicknames}")

        # Enter room pin
        room_pin = client.recv(1024).decode("ascii")
        status = "false"
        current_room = None
        for room in rooms:
            if(int(room_pin) == room.pin):
                current_room = room
                status = "true"
                break

        while status != "true":
            client.send("false".encode("ascii"))
            room_pin = client.recv(1024).decode("ascii")
            for room in rooms:
                if(int(room_pin) == room.pin):
                    current_room = room
                    status = "true"
                    break

        player = Player(nickname, address, current_room)
        current_room.players.append(player)
        print(f"Current room: {current_room}")
        client.send("true".encode("ascii"))

        print(f"Current player in room {current_room.pin}")
        for player in current_room.players:
            print(f"{player.nickname}")

        print("Waiting for host to start game!!!!")
        while(current_room.state != State.START_GAME):
            # print(current_room.state)
            pass
        print("Game started")
        client.send("Game started".encode("ascii"))

        confirm = client.recv(1024).decode("ascii") # Receive confirm
        print(confirm)
        # --------------------------------Game started---------------------------------
        noAns = current_room.quiz.noAns
        print(current_room.quiz.noAns)
        # print(type(current_room.quiz.noAns))
        client.send(str(noAns).encode("ascii")) # 
        for x in range(0,current_room.quiz.noQuest):
            while(current_room.state != State.NEXT_QUEST and current_room.state != State.SHOW_QUESTION):
                # print(current_room.state)
                pass 
            client.send("Choose anwser".encode("ascii")) # Display next question

            answer = client.recv(1024).decode("ascii") # Receive answer
            while(current_room.state != State.SHOW_RESULT):
                pass 
            client.send("Result".encode("ascii")) # Show result

        client.send("End".encode("ascii"))

        print("ServerPlayer end game")
        


    except:
        clients.remove(client)
        client.close()

def main():
    # try:
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        role = client.recv(1024).decode("ascii")
        clients.append(client)

        if(role == "1"): #Host
            client.send("Connected to the server".encode("ascii"))

            thread = threading.Thread(target=handleHost, args=(client, address, ), daemon=True)
            thread.start()
        else: #Player
            client.send("Connected to the server".encode("ascii"))

            thread = threading.Thread(target=handlePlayer, args=(client, address, ), daemon=True)
            thread.start()

            # while thread.is_alive():
            #     thread.join(1)
    # except KeyboardInterrupt:
    #     print("Ctrl+C pressed...")
    #     sys.exit(1)
        

print("Server is listening...")
if __name__ == "__main__":
    main()
