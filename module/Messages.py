
from module.MessType import MessType


class Messages():
    def __init__(self, type: str, username: str = "none", hash: str = "none",state: bool = True, body: str = "none"):
        self.type = type
        self.username = username
        self.hash = hash
        self.state = state
        self.header = f"{type};{username};{hash};{state}"
        self.body = body

    def to_message(self):
        return f"{str(self.header)}\n{str(self.body)}" 

def convert_message(message: str) -> Messages:
    header, body = message.split("\n")
    # print(header)
    # print(body)
    type, username, hash, state = header.split(";")
    # print("---")
    # print(type)
    # print(username)
    # print(hash)
    # print(state)

    return Messages(type, username, hash, state, body)
# a = Messages(MessType.CONFIRM_ROLE)
# mess = a.to_message()
# print(mess)
# print(mess.split(";"))