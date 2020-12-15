import json

class Quiz():
    def __init__(self, name, noQuest, noAns, questions, answers, rights ):
        self.name = name
        self.noQuest = noQuest
        self.noAns = noAns
        self.questions = questions
        self.answers = answers
        self.rights = rights





def data_to_quiz():
    f = open("data.json")
    quizzes = json.load(f)
    quizzesClasses = []   
    for quiz in quizzes:
        questions = []
        answers = []
        rights = []
        name  = quiz['name']
        noQuest  = quiz['noQuest']
        noAns = quiz['noAns']
        lists = quiz['lists']

        for list in lists:
            quest = list['quest']
            questions.append(quest)

            ans = list['ans']
            answers.append(ans)

            right = list['right']
            rights.append(right)
        
        quizzesClass = Quiz(name, noQuest, noAns, questions, answers, rights)
        quizzesClasses.append(quizzesClass)
        # for u in quizzesClasses:
        #     print(u.name)
        #     print(u.noQuest)
        #     print(u.noAns)
        #     print(u.questions[0])
        #     print(u.answers[0])
        #     print(u.rights[0])

    return quizzesClasses
# data_to_quiz()    

