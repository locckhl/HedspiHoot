from module.MessType import MessType
from module.Messages import Messages
from clients.playerClient import playerClient
from clients.hostClient import hostClient
from module.Quiz import Quiz, data_to_quiz
import socket
import threading
import sys
import json
import time
import ast
from env import CLIENT_IP

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((CLIENT_IP, 55555))



def main():
    # try:
    print("--------------Welcome to HedHoot!!!!--------------")
    print("1. I want to be a Host:")
    print("2. I want to be a Player:")
    print("3. Bye bye")
    role = input("Please choose your choice ")
    

    while(role != "3"):
        client.send(Messages(MessType.SEND_ROLE.name, body=role).to_message())
        if(role == "1"): #Host
            hostClient(client)
        else: #Player
            playerClient(client)

        print("--------------Welcome to HedHoot!!!!--------------")
        print("1. I want to be a Host:")
        print("2. I want to be a Player:")
        print("3. Bye bye")
        role = input("Please choose your choice ")

    print("Good bye")
    # username = input("Welcome to HedHoot, please username")
    # client.send(Messages(MessType.NEW_QUIZ.name, username,"asdfa", False, "{dfs,wf,wf}").to_message())
    # client.close()
    # except:
    #     print("An error occured")
    #     client.close()
    #     sys.exit(1)


print("Server is listening...")
if __name__ == "__main__":
    main()