import json
from itertools import count
class Quiz():
    id_iter = count()

    def __init__(self, name, noQuest, noAns, questions, answers, rights ):
        self.name = name
        self.noQuest = noQuest
        self.noAns = noAns
        self.questions = questions
        self.answers = answers
        self.rights = rights
        self.id = self.id = next(Quiz.id_iter)

    def to_string(self):
        return f"{str(self.id)};{str(self.id2)};{str(self.id3)}"  


def append_data_json(new_data):

    with open('data.json') as f:
        data = json.load(f)

    data.append(new_data)

    with open('data.json', 'w') as f:
        json.dump(data, f)
    
    # the result is a JSON string: 

def package_to_data(name, noQuest, noAns, questions, answers, rights):
    print(name, noQuest, noAns, questions, answers, rights )
    result = {}
    result.update({"name":name})
    result.update({"noQuest":noQuest})
    result.update({"noAns":noAns})
    result.update({"lists":[]})

    for (a, b, c) in zip(questions, answers, rights): 
        # print (f"a, b, c:{a};{b};{c}")
        # temp_result = result
        result["lists"].append({"quest":a,"ans":b,"right":c})
        # print(result["lists"])
    # print(result)
    return result

def quiz_package_handle(name, noQuest, noAns, questions, answers, rights):
    new_data = package_to_data(name, noQuest, noAns, questions, answers, rights)
    append_data_json(new_data)

def data_to_quiz(filename):
    f = open(filename)
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
    #2 2 2 ['2', '2'] [['2', '2'], ['2', '2']] [1, 1]
# data_to_quiz()    
# append_data_json({ "name": "Math", "noQuest": 2, "noAns": 2, "lists": [ { "quest": "1+1 = ?", "ans": [2, 3], "right": 0 }, { "quest": "1-1 = ?", "ans": [0, 45], "right": 0 } ] })
# a = package_to_data(2, 2, 2, ['2', '2'], [['2', '2'], ['2', '2']], [1, 1])
# print(a)
# append_data_json(a)

# quiz1 = Quiz(1, 2, 3, 4, 5, 6 )
# quiz2 = Quiz(1, 2, 3, 4, 5,6)
# print(quiz1.id)
# print(quiz2.id)
