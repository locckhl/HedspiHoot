import socket
import threading
import sys


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.31.124", 55555))


def hostClient():
    pin = client.recv(1024).decode("ascii")
    print(pin)

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