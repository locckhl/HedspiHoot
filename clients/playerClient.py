from inputimeout import inputimeout, TimeoutOccurred
from env import TIME

def playerClient(client):
    # Receive confirm from server: you are ...
    message = client.recv(1024).decode("ascii")
    print(message)

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
    status = client.recv(1024).decode("ascii") # was an available room ?

    while status == "false":
        pin = input("Room not found, please input another one: ")
        client.send(pin.encode("ascii"))
        status = client.recv(1024).decode("ascii") # was an available room ?
    print(f"Your enter room: {pin} ")

    print("Waiting for host to start game!!!!")
    client.recv(1024).decode("ascii")
    print("Game started")

    client.send("CONFIRM".encode("ascii"))

    # --------------------------------Game started---------------------------------

    noAns = client.recv(1024).decode("ascii")
    client.send("nop".encode("ascii"))
    print(f"noAns:{noAns}")
    mess = client.recv(1024).decode("ascii")
    print(f"mess from server:{mess}")
    while(mess != 'End'):

        print("Please choose Answers")
        for x in range(0,int(noAns)):
            print(f"{x+1}.")
        # answer = input("Your anwer >> ")
        try:
            answer = inputimeout(prompt=f'You have {TIME} seconds to answer:', timeout=TIME)
        except TimeoutOccurred:
            print("You missed this question")
            answer = '0'
        client.send(answer.encode("ascii"))
        result = client.recv(1024).decode("ascii")
        print(result)
        client.send("nop".encode("ascii"))
        mess = client.recv(1024).decode("ascii")
    print("End game")
    client.close()
