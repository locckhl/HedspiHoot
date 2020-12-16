from module.Quiz import data_to_quiz
import socket
import threading
import sys
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.31.124", 55555))


def hostClient():
    client.send("nop".encode("ascii"))
    pin = client.recv(1024).decode("ascii")
    print(f"received pin:{pin}")
    # print(pin)


    choice = input("Do you wan to create new quiz (1) or choose from our quizzes (2) : ")
    client.send(choice.encode("ascii"))

    if(choice  == "1"):
        # Send quiz
        client.recv(1024).decode('ascii') # nop

        name = input("Please input quiz's name: ")
        noQuest = int(input("Please input quiz's noQuest: "))
        noAns = int(input("Please input quiz's noAns: "))

        questions = []
        answers = []
        rights = []

        for x in range(0,noQuest):
            quest = input(f"Please input question{x+1}: ")
            questions.append(quest)

            each_answer = []    
            for y in range(0,noAns):
                ans = input(f"\tPlease input ans {y+1} of question {x+1}: ")
                each_answer.append(ans)
                
            answers.append(each_answer)

            right = int(input(f"Please input right answer of question {x+1} (1 to {noAns}): ")) - 1
            rights.append(right)

        client.send(f"{name};{noQuest};{noAns};{questions};{answers};{rights}".encode("ascii"))
    else:
        data = client.recv(1024).decode('ascii') # receive data.json
        data = data.replace("\'", "\"")
        print(f"data:{data}")
        f = open("data-client.json", "w")
        f.write(data)
        f.close()
        quizzes = data_to_quiz("data-client.json")
        print(f"quizzes:{quizzes}")

        print("Choose a quiz")
        for quiz in quizzes:
            print(f"{quiz.id + 1}.: {quiz.name}")
        choice = input("Your choice:")
        # send choice
        client.send(choice.encode("ascii"))


def playerClient():
    nickname = input("Please input your nickname: ")
    client.send(nickname.encode("ascii"))
    status = client.recv(1024).decode("ascii") # was nickname created sucessfully

    while status == "false":
        nickname = input("Your nick name was taken, please input another one: ")
        client.send(nickname.encode("ascii"))
        status = client.recv(1024).decode("ascii") # was nickname created sucessfully
    print(f"Your nick name {nickname} was created sucessfully")

    pin = input("Input a room's pin: ")
    client.send(pin.encode("ascii"))
    status = client.recv(1024).decode("ascii") # was an available room

    while status == "false":
        pin = input("Room not found, please input another one: ")
        client.send(pin.encode("ascii"))
        status = client.recv(1024).decode("ascii") # was an available room
    print(f"Your enter room: {pin} ")

def main():
    try:
        role = input("Welcome to HedHoot, please choose your role\n 1. Host\n 2. Player: ")
        client.send(role.encode("ascii"))
        message = client.recv(1024).decode("ascii")
        print(message)
        message = client.recv(1024).decode("ascii")
        print(message)
        print(role)

        if(role == "1"): #Host
            hostClient()
        else: #Player
            playerClient()
            

    except:
        print("An error occured")
        client.close()
        sys.exit(1)


print("Server is listening...")
if __name__ == "__main__":
    main()