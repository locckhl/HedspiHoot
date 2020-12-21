from module.Quiz import Quiz, data_to_quiz
from inputimeout import inputimeout, TimeoutOccurred
import ast
from env import TIME

def hostClient(client):
    # Receive confirm from server: you are ...
    message = client.recv(1024).decode("ascii")
    print(message)

    # client.send("nop".encode("ascii"))
    
    # print(pin)

    choice = input("Do you wan to create new quiz (1) or choose from our quizzes (2) : ")
    client.send(choice.encode("ascii"))

    if(choice  == "1"):
        # Send quiz
        client.recv(1024).decode("ascii") # nop

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
        current_quiz = Quiz(name, int(noQuest), int(noAns), questions, answers, rights)
    else:
        data = client.recv(1024).decode("ascii") # receive data.json
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
        client.send(choice.encode("ascii"))

        received_quiz = client.recv(1024).decode("ascii") 
        # print(received_quiz)
        name, noQuest, noAns, questions, answers, rights = received_quiz.split(';')
        
        client.send("nop".encode("ascii"))
        current_quiz = Quiz(name, int(noQuest), int(noAns), ast.literal_eval(questions), ast.literal_eval(answers), ast.literal_eval(rights))

    
    print(f"current_quiz:{current_quiz.to_string()}")
    # print(f"current_quiz2:{current_quiz.questions[0]}")

    # Received pin
    pin = client.recv(1024).decode("ascii")
    print(f"received pin:{pin}")
    client.send("nop".encode("ascii"))
    

    # Waiting for players
    current_players = client.recv(1024).decode("ascii") 
    request_start_game = 'n'

    try:
        request_start_game = inputimeout(prompt=f'Current player is {current_players}, do you want to start game (y or n ): ', timeout=2)
    except TimeoutOccurred:
        pass

    while request_start_game != "y":
        client.send("n".encode("ascii"))
        current_players = client.recv(1024).decode("ascii") 
        # if current_players != temp:
        #     current_players = temp
        # request_start_game = input(f"Current player is {current_players}, do you want to start game (y or n ): ")
        try:
            request_start_game = inputimeout(prompt=f'Current player is {current_players}, do you want to start game (y or n ): ', timeout=3)
        except TimeoutOccurred:
            pass
    
    client.send("y".encode("ascii"))
    print("Game started")
    
    # --------------------------------Game started---------------------------------
    print(current_quiz.noQuest)
    for x in range(0,current_quiz.noQuest):
        print(x)
        mess = client.recv(1024).decode("ascii") 
        print(mess)
        # Show questions and answers
        # mess = client.recv(1024).decode("ascii") 
        # print(mess)
        print(f"Question {x+1}: {current_quiz.questions[x]}")
        for y in  range(0,current_quiz.noAns):
            print(f"Answer {y+1}: {current_quiz.answers[x][y]}")

        mess = client.recv(1024).decode("ascii") 
        print(mess)
        if(x != (current_quiz.noQuest-1)):
            request_next_quest = input("Next question (type y)?")
            client.send(request_next_quest.encode("ascii"))
        else:
            client.send("End of quiz".encode("ascii"))
    print("End game")
    client.close()
