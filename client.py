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
    role = input("Welcome to HedHoot, please choose your role\n 1. Host\n 2. Player: ")
    client.send(role.encode("ascii"))
    
    # client.send("nop".encode("ascii"))
    # message = client.recv(1024).decode("ascii")
    # print(message)
    # print(role)

    if(role == "1"): #Host
        hostClient(client)
    else: #Player
        playerClient(client)
            

    # except:
    #     print("An error occured")
    #     client.close()
    #     sys.exit(1)


print("Server is listening...")
if __name__ == "__main__":
    main()