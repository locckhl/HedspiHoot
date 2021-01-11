from module.MessType import MessType
from module.Messages import Messages, convert_message
from inputimeout import inputimeout, TimeoutOccurred
from env import TIME

def playerClient(client):
    # Receive confirm from server: you are ...
    message = convert_message(client.recv(1024)).body
    print(message)

    nickname = input("Please input your nickname: ")
    client.send(Messages(MessType.SET_NICKNAME.name, body=f"{nickname}").to_message())

    status = convert_message(client.recv(1024)).body # was nickname created sucessfully

    while status == "false":
        nickname = input("Your nick name was taken, please input another one: ")
        client.send(Messages(MessType.SET_NICKNAME.name, body=f"{nickname}").to_message())
        status = convert_message(client.recv(1024)).body # was nickname created sucessfully
    print(f"Your nick name {nickname} was created sucessfully")

    print("Input a room's pin to play: ")
    print("Enter 0 to exit: ")
    pin = input(">> ")
    while pin != "0":
        client.send(Messages(MessType.ROOM_PIN.name, username=nickname, body=f"{pin}").to_message())
        status = convert_message(client.recv(1024)).body # was an available room ?

        while status == "false":
            pin = input("Room not found, please input another one: ")
            client.send(Messages(MessType.ROOM_PIN.name, username=nickname, body=f"{pin}").to_message())
            status = convert_message(client.recv(1024)).body # was an available room ?
        print(f"Your enter room: {pin} ")

        print("Waiting for host to start game!!!!")
        noAns, mess = convert_message(client.recv(1024)).body.split(";")
        print("Game started")

        # --------------------------------Game started---------------------------------
        # print(f"noAns:{noAns}")
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
            client.send(Messages(MessType.SEND_ANSWER.name, username=nickname, body=f"{pin};{answer}").to_message())
            status = convert_message(client.recv(1024)).body
            print(status)
            mess = convert_message(client.recv(1024)).body
        print("End game")
        client.close()

        print("Input a room's pin to continue play: ")
        print("Enter 0 to exit: ")
        pin = input(">> ")
    print("Return to main menu")