

class Package():
    def __init__(self,):
        self.id = 123
        self.id2 = [
            {"who are you":[1,2,3,4]},
            {"where is the sun":["here","there","idk","..."]},
        ]
        self.id3 = 124

    def to_string(self):
        return f"{str(self.id)};{str(self.id2)};{str(self.id3)}"    

    
a = Package()
mess = a.to_string()
# print(dir(a))
print(mess.split(";"))