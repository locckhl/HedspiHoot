from module.MessType import MessType
from module.Messages import Messages, convert_message
from module.Quiz import Quiz, data_to_quiz
from inputimeout import inputimeout, TimeoutOccurred
import ast
from env import TIME

def hostClient(client):
    # Receive confirm from server: you are ...
    rmessage = convert_message(client.recv(1024)) # print received message
    print(rmessage.body)

    print("1. Sign up: ")
    print("2. Sign in: ")
    print("3. Return to main menu: ")

    choice = input(">>>")

    while choice != "3":
        client.send(Messages(MessType.HOST_SIGN.name, body=choice).to_message())

        if(choice == "1"): #sign up
            username = input("Input username : ")
            password = input("Input password : ")
            confirm_password = input("Confirm password : ")
            client.send(Messages(MessType.SIGN_UP.name, body=f"{username};{password};{confirm_password}").to_message())
            rmessage = convert_message(client.recv(1024)) # print received message
            print(rmessage.body)
            while rmessage.state != "True":
                username = input("Input username : ")
                password = input("Input password : ")
                confirm_password = input("Confirm password : ")
                client.send(Messages(MessType.SIGN_UP.name, body=f"{username};{password};{confirm_password}").to_message())
                rmessage = convert_message(client.recv(1024)) # print received message
                print(rmessage.body)
        else: # sign in
            username = input("Input username : ")
            password = input("Input password : ")
            client.send(Messages(MessType.SIGN_IN.name, body=f"{username};{password}").to_message())
            rmessage = convert_message(client.recv(1024)) # print received message
            print(rmessage.body)
            while rmessage.state != "True":
                username = input("Input username : ")
                password = input("Input password : ")
                client.send(Messages(MessType.SIGN_IN.name, body=f"{username};{password}").to_message())
                rmessage = convert_message(client.recv(1024)) # print received message
                print(rmessage.body)
                
        choice = input("Do you wan to create new quiz (1) or choose from our quizzes (2) : ")
        client.send(Messages(MessType.NEW_QUIZ.name, username=username, body=choice).to_message())

        if(choice  == "1"):
            # Send quiz
            rmessage = convert_message(client.recv(1024))
            print(rmessage.body)

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

            client.send(Messages(MessType.SEND_NEW_QUIZ.name, username=username, body=f"{name};{noQuest};{noAns};{questions};{answers};{rights}").to_message())
            current_quiz = Quiz(name, int(noQuest), int(noAns), questions, answers, rights)
        else:
            data = convert_message(client.recv(4096)).body # receive data.json
            if data == "[]":
                print("You dont have any quiz yet")
                print("Create a new on")
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

                client.send(Messages(MessType.SEND_NEW_QUIZ.name, username=username, body=f"{name};{noQuest};{noAns};{questions};{answers};{rights}").to_message())
                current_quiz = Quiz(name, int(noQuest), int(noAns), questions, answers, rights, username)
            else:
                data = data.replace("\'", "\"")
                f = open("data-client.json", "w")
                f.write(data)
                f.close()
                quizzes = data_to_quiz("data-client.json")
                # print(f"quizzes:{quizzes}")

                print("Choose a quiz")
                for quiz in quizzes:
                    print(f"{quiz.id + 1}.: {quiz.name}")
                choice = input("Your choice:")
                # send choice
                client.send(Messages(MessType.SEND_QUIZ_CHOICE.name, username=username, body=choice).to_message())

                received_quiz = convert_message(client.recv(1024)).body
                # print(received_quiz)
                name, noQuest, noAns, questions, answers, rights, user = received_quiz.split(';')
                
                current_quiz = Quiz(name, int(noQuest), int(noAns), ast.literal_eval(questions), ast.literal_eval(answers), ast.literal_eval(rights), user)

        
        print(f"current_quiz:{current_quiz.to_string()}")
        # print(f"current_quiz2:{current_quiz.questions[0]}")

        # Received pin
        pin = convert_message(client.recv(1024)).body
        print(f"received pin:{pin}")
        
        client.send(Messages(MessType.REQUEST_START_GAME.name,username=username, body="n").to_message())

        # Waiting for players
        request_start_game = 'n'
        current_players = convert_message(client.recv(1024)).body

        try:
            request_start_game = inputimeout(prompt=f'Current player is {current_players}, do you want to start game (y or n ): ', timeout=2)
        except TimeoutOccurred:
            pass

        while request_start_game != "y":
            client.send(Messages(MessType.REQUEST_START_GAME.name, username=username, body="n").to_message())
            current_players = convert_message(client.recv(1024)).body
            # if current_players != temp:
            #     current_players = temp
            # request_start_game = input(f"Current player is {current_players}, do you want to start game (y or n ): ")
            try:
                request_start_game = inputimeout(prompt=f'Current player is {current_players}, do you want to start game (y or n ): ', timeout=3)
            except TimeoutOccurred:
                pass
        
        client.send(Messages(MessType.REQUEST_START_GAME.name, username=username, body="y").to_message())
        print("Game started")
        
        # --------------------------------Game started---------------------------------
        print(current_quiz.noQuest)
        for x in range(0,current_quiz.noQuest):
            print(x)
            mess = convert_message(client.recv(1024)).body
            print(mess)
            # client.send(Messages(MessType.CONFIRM_ROLE.name, body="ok").to_message())
            # Show questions and answers
            # mess = convert_message(client.recv(1024)).body
            # print(mess)
            print(f"Question {x+1}: {current_quiz.questions[x]}")
            for y in  range(0,current_quiz.noAns):
                print(f"Answer {y+1}: {current_quiz.answers[x][y]}")

            mess = convert_message(client.recv(1024)).body
            print(mess)
            if(x != (current_quiz.noQuest-1)):
                request_next_quest = input("Next question (type y)?")
                client.send(Messages(MessType.REQUEST_NEXT_QUESTION.name, username=username, body=request_next_quest).to_message())
            else:
                client.send(Messages(MessType.END_GAME.name, username=username, body="End game").to_message())
        print("End game")
        client.close()

        print("1. Sign up: ")
        print("2. Sign in: ")
        print("3. Return to main menu: ")

        choice = input(">>>")
    print("Return to main menu")

